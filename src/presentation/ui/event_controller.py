"""Module for handling UI events in the Canny Edge Detection application."""

import os
import io
import cv2
import numpy as np
import PySimpleGUI as sg
from PIL import Image, ImageTk

from ...services.image_processing_service import ImageProcessingService
from ...services.image_conversion_service import ImageConversionService
from ...name_convention import UIVariables
from ...config import (
    SUPPORTED_FORMATS,
    UI_FONT,
    TEMP_IMAGE_FILE,
    TRANSFORM_IMAGE_FILE,
    EMPTY_IMAGE_PATH
)
from ...logger import logger

class EventController:
    """Handles all UI events and their associated logic."""

    def __init__(self, window):
        """Initialize controller with window and required components."""
        self.window = window
        self.ui_vars = UIVariables()
        self.image_processor = ImageProcessingService()
        self.image_converter = ImageConversionService()
        self.folder = None
        self.total_objects = 0

    def handle_event(self, event, values):
        """Handle UI events."""
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
        self._cleanup_temp_files()
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

        self._reset_state()

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
            self._clear_image_viewer()
            self.total_objects += self.image_processor.current_objects

        self.window["-OBJECTS-"].update(
            f"Total Number of Objects Detected from Images in Folder: {self.total_objects}"
        )

    def _handle_file_selection(self, values):
        """Handle file selection from the list."""
        if not values["-FILE LIST-"]:
            return
            
        try:
            self._clear_transformations()
            file_path = os.path.join(self.folder, values["-FILE LIST-"][0])
            min_val = int(values['-cannyMinValue-'])
            max_val = int(values['-cannyMaxValue-'])
            
            self._process_image(file_path, min_val, max_val)
            self._show_main_image(TEMP_IMAGE_FILE)
            self._display_transformations()
            
            self.window["-num_of_objects-"].update(
                f"Total number of objects detected in selected image: {self.image_processor.current_objects}"
            )
        except Exception as e:
            logger.error(f"Error handling file selection: {str(e)}")

    def _process_image(self, filepath, min_val, max_val):
        """Process a single image through the edge detection pipeline."""
        self.image_converter.convert_to_png(filepath, TEMP_IMAGE_FILE)
        self.image_processor.process_image(TEMP_IMAGE_FILE, min_val, max_val)

    def _display_transformations(self):
        """Display all image transformations in the UI."""
        # Show blurred image
        cv2.imwrite(TRANSFORM_IMAGE_FILE, self.image_processor.blurred_image)
        self._show_transformation(
            self.ui_vars.first_transformation,
            self.ui_vars.blur_image,
            ""
        )

        # Show edge detection
        cv2.imwrite(TRANSFORM_IMAGE_FILE, self.image_processor.edges)
        self._show_transformation(
            self.ui_vars.first_transformation,
            self.ui_vars.edges_image,
            "Gaussian Blurred, Grayscaled Image, \n and Edges Detected through Canny Algorithm (left to right):"
        )

        # Show dilated edges
        cv2.imwrite(TRANSFORM_IMAGE_FILE, self.image_processor.dilated_edges)
        self._show_transformation(
            self.ui_vars.second_transformation,
            self.ui_vars.dilated_edges_image,
            ""
        )

        # Show contours
        result = np.zeros_like(self.image_processor.image)
        cv2.drawContours(
            result,
            self.image_processor.contours,
            -1,
            (0, 255, 0),
            thickness=-1
        )
        cv2.imwrite(TRANSFORM_IMAGE_FILE, result)
        self._show_transformation(
            self.ui_vars.second_transformation,
            self.ui_vars.contours_image,
            "Dilated Edges, \n and External Contours Filled (left to right):"
        )

    def _show_transformation(self, transform_name, transform_image, description):
        """Display a transformation step in the UI."""
        try:
            logger.debug(f"Showing transformation: {transform_name}")
            self.image_converter.resize_image(TRANSFORM_IMAGE_FILE, TRANSFORM_IMAGE_FILE, 320, 240)
            image = Image.open(TRANSFORM_IMAGE_FILE)
            self.window[transform_name].update(description)
            self.window[transform_image].update(data=ImageTk.PhotoImage(image))
        except Exception as e:
            logger.error(f"Error showing transformation {transform_name}: {str(e)}")
            raise

    def _show_main_image(self, file_path):
        """Display the main image in the UI."""
        try:
            logger.debug(f"Displaying image: {file_path}")
            self.image_converter.resize_image(file_path, file_path, 320, 240)
            image = Image.open(file_path)
            bio = io.BytesIO()
            image.save(bio, "PNG")
            self.window["-IMAGE-"].update(data=bio.getvalue())
        except Exception as e:
            logger.error(f"Error displaying image {file_path}: {str(e)}")
            raise

    def _clear_image_viewer(self):
        """Clear the image displayed in the viewer."""
        try:
            logger.debug("Clearing main image viewer")
            self.image_converter.resize_image(EMPTY_IMAGE_PATH, TEMP_IMAGE_FILE, 320, 240)
            self._show_main_image(TEMP_IMAGE_FILE)
        except Exception as e:
            logger.error(f"Error clearing image viewer: {str(e)}")
            raise

    def _clear_transformations(self):
        """Clear all transformation displays."""
        logger.debug("Clearing transformation displays")
        for key in [
            self.ui_vars.first_transformation,
            self.ui_vars.second_transformation,
            self.ui_vars.blur_image,
            self.ui_vars.edges_image,
            self.ui_vars.dilated_edges_image,
            self.ui_vars.contours_image,
            "-num_of_objects-"
        ]:
            self.window[key].update('')

    def _reset_state(self):
        """Reset the controller state."""
        logger.info("Resetting controller state")
        self._clear_transformations()
        self.window["-FILE LIST-"].update('')
        self.total_objects = 0

    def _cleanup_temp_files(self):
        """Remove temporary image files."""
        logger.debug("Cleaning up temporary files")
        temp_files = [TEMP_IMAGE_FILE, TRANSFORM_IMAGE_FILE]
        for file_name in temp_files:
            if os.path.exists(file_name):
                try:
                    os.remove(file_name)
                    logger.debug(f"Removed temporary file: {file_name}")
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file {file_name}: {str(e)}")