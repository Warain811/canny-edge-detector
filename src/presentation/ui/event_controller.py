"""Module for handling UI events in the Canny Edge Detection application."""

import os
import cv2
import numpy as np
import PySimpleGUI as sg

from ...open_image import ImageViewer
from ...canny_edge_detector import EdgeDetector
from ...name_convention import UIVariables
from ...config import (
    SUPPORTED_FORMATS,
    UI_FONT,
    TEMP_IMAGE_FILE,
    TRANSFORM_IMAGE_FILE
)

class EventController:
    """Handles all UI events and their associated logic."""

    def __init__(self, window):
        """Initialize controller with window and required components.
        
        Args:
            window: PySimpleGUI window instance
        """
        self.window = window
        self.ui_vars = UIVariables()
        self.image_viewer = ImageViewer(window)
        self.edge_detector = EdgeDetector()
        self.folder = None

    def handle_event(self, event, values):
        """Handle UI events.
        
        Args:
            event: The event triggered in the UI
            values: Dictionary of values from UI elements
            
        Returns:
            bool: True if the application should continue, False if it should exit
        """
        if event in (sg.WIN_CLOSED, "Exit"):
            return False

        handlers = {
            "Browse": self._handle_browse,
            "Load Images\n and Detect Objects": self._handle_load_images,
            "-FILE LIST-": self._handle_file_selection
        }

        if event in handlers:
            handlers[event](values)
        
        return True

    def cleanup(self):
        """Perform cleanup operations before exit."""
        self.image_viewer.cleanup_temp_files()
        self.window.close()

    def _handle_browse(self, values):
        """Handle Browse button click."""
        file_path = sg.popup_get_folder(no_window=True, message="")
        if file_path:
            self.window['-FOLDER-'].update(file_path)
        else:
            sg.Popup(
                "Please choose a folder. Program will use previously loaded folder.",
                font=UI_FONT,
                button_type=5,
                title="Error!"
            )

    def _handle_load_images(self, values):
        """Handle Load Images and Detect Objects button click."""
        self.folder = values['-FOLDER-']
        if not self.folder:
            sg.Popup(
                "Please choose a nonempty folder. Program will use previously loaded folder.",
                font=UI_FONT,
                button_type=5,
                title="Error!"
            )
            return

        min_val = int(values['-cannyMinValue-'])
        max_val = int(values['-cannyMaxValue-'])

        if min_val > max_val:
            sg.Popup(
                "Min value cannot exceed max value.",
                font=UI_FONT,
                button_type=5,
                title="Error!"
            )
            return

        self.image_viewer.reset()
        self.edge_detector.reset_total_objects()

        try:
            file_names = [
                f for f in os.listdir(self.folder)
                if os.path.isfile(os.path.join(self.folder, f))
                and f.lower().endswith(SUPPORTED_FORMATS)
            ]
        except:
            file_names = []

        if not file_names:
            sg.Popup(
                "Chosen folder is empty. Please choose a different folder",
                font=UI_FONT,
                button_type=5,
                title="Warning!"
            )
            return

        self.window["-FILE LIST-"].update(file_names)

        for file_name in file_names:
            file_path = os.path.join(self.folder, file_name)
            self._process_image(file_path, min_val, max_val)
            self.image_viewer.clear_image_in_image_viewer()
            self.edge_detector.update_total_objects()

        self.window["-OBJECTS-"].update(
            f"Total Number of Objects Detected from Images in Folder: {self.edge_detector.total_objects}"
        )

    def _handle_file_selection(self, values):
        """Handle file selection from the list."""
        if not values["-FILE LIST-"]:
            return
            
        try:
            self.image_viewer.clear_info()
            file_path = os.path.join(self.folder, values["-FILE LIST-"][0])
            min_val = int(values['-cannyMinValue-'])
            max_val = int(values['-cannyMaxValue-'])
            
            self._process_image(file_path, min_val, max_val)
            self.image_viewer.show_image(TEMP_IMAGE_FILE)
            self._display_transformations()
            
            self.window["-num_of_objects-"].update(
                f"Total number of objects detected in selected image: {self.edge_detector.current_objects}"
            )
        except:
            pass

    def _process_image(self, filepath, min_val, max_val):
        """Process a single image through the edge detection pipeline."""
        # Convert and display original image
        self.image_viewer.convert_to_png(filepath)
        
        # Process edges
        self.edge_detector.detect_edges(TEMP_IMAGE_FILE, min_val, max_val)

    def _display_transformations(self):
        """Display all image transformations in the UI."""
        # Show blurred image
        cv2.imwrite(TRANSFORM_IMAGE_FILE, self.edge_detector.blurred_image)
        self.image_viewer.show_transformation(
            self.ui_vars.first_transformation,
            self.ui_vars.blur_image,
            ""
        )

        # Show edge detection
        cv2.imwrite(TRANSFORM_IMAGE_FILE, self.edge_detector.edges)
        self.image_viewer.show_transformation(
            self.ui_vars.first_transformation,
            self.ui_vars.edges_image,
            "Gaussian Blurred, Grayscaled Image, \n and Edges Detected through Canny Algorithm (left to right):"
        )

        # Show dilated edges
        cv2.imwrite(TRANSFORM_IMAGE_FILE, self.edge_detector.dilated_edges)
        self.image_viewer.show_transformation(
            self.ui_vars.second_transformation,
            self.ui_vars.dilated_edges_image,
            ""
        )

        # Show contours
        result = np.zeros_like(self.edge_detector.image)
        cv2.drawContours(
            result,
            self.edge_detector.contours,
            -1,
            (0, 255, 0),
            thickness=-1
        )
        cv2.imwrite(TRANSFORM_IMAGE_FILE, result)
        self.image_viewer.show_transformation(
            self.ui_vars.second_transformation,
            self.ui_vars.contours_image,
            "Dilated Edges, \n and External Contours Filled (left to right):"
        )