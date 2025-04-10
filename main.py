"""Main module for the Canny Edge Detection application."""

import os
import cv2
import numpy as np
import PySimpleGUI as sg

from src.open_image import ImageViewer
from src.canny_edge_detector import EdgeDetector
from src.name_convention import UIVariables
from src.presentation.ui.layout import create_window
from src.config import (
    ASSETS_DIRECTORY,
    SUPPORTED_FORMATS,
    UI_FONT,
    TEMP_IMAGE_FILE,
    TRANSFORM_IMAGE_FILE
)

def create_directory_structure():
    """Create necessary directories if they don't exist."""
    for directory in [ASSETS_DIRECTORY]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def process_edges(edge_detector, filepath, min_val, max_val):
    """Process image edges using the Canny edge detection pipeline."""
    edge_detector.detect_edges(filepath, min_val, max_val)
    return edge_detector

def display_transformations(image_viewer, edge_detector, ui_vars):
    """Display all image transformations in the UI."""
    # Show blurred image
    cv2.imwrite(TRANSFORM_IMAGE_FILE, edge_detector.blurred_image)
    image_viewer.show_transformation(
        ui_vars.first_transformation,
        ui_vars.blur_image,
        ""
    )

    # Show edge detection
    cv2.imwrite(TRANSFORM_IMAGE_FILE, edge_detector.edges)
    image_viewer.show_transformation(
        ui_vars.first_transformation,
        ui_vars.edges_image,
        "Gaussian Blurred, Grayscaled Image, \n and Edges Detected through Canny Algorithm (left to right):"
    )

    # Show dilated edges
    cv2.imwrite(TRANSFORM_IMAGE_FILE, edge_detector.dilated_edges)
    image_viewer.show_transformation(
        ui_vars.second_transformation,
        ui_vars.dilated_edges_image,
        ""
    )

    # Show contours
    result = np.zeros_like(edge_detector.image)
    cv2.drawContours(
        result,
        edge_detector.contours,
        -1,
        (0, 255, 0),
        thickness=-1
    )
    cv2.imwrite(TRANSFORM_IMAGE_FILE, result)
    image_viewer.show_transformation(
        ui_vars.second_transformation,
        ui_vars.contours_image,
        "Dilated Edges, \n and External Contours Filled (left to right):"
    )

def process_image(image_viewer, edge_detector, filepath, min_val, max_val, ui_vars):
    """Process a single image through the edge detection pipeline."""
    # Convert and display original image
    image_viewer.convert_to_png(filepath)
    
    # Process edges
    process_edges(edge_detector, TEMP_IMAGE_FILE, min_val, max_val)

def main():
    """Main application entry point."""
    create_directory_structure()
    ui_vars = UIVariables()
    window = create_window()
    image_viewer = ImageViewer(window)
    edge_detector = EdgeDetector()

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, "Exit"):
            break

        elif event == "Browse":
            file_path = sg.popup_get_folder(no_window=True, message="")
            if file_path:
                window['-FOLDER-'].update(file_path)
            else:
                sg.Popup(
                    "Please choose a folder. Program will use previously loaded folder.",
                    font=UI_FONT,
                    button_type=5,
                    title="Error!"
                )

        elif event == "Load Images\n and Detect Objects":
            folder = values['-FOLDER-']
            if not folder:
                sg.Popup(
                    "Please choose a nonempty folder. Program will use previously loaded folder.",
                    font=UI_FONT,
                    button_type=5,
                    title="Error!"
                )
                continue

            min_val = int(values['-cannyMinValue-'])
            max_val = int(values['-cannyMaxValue-'])

            if min_val > max_val:
                sg.Popup(
                    "Min value cannot exceed max value.",
                    font=UI_FONT,
                    button_type=5,
                    title="Error!"
                )
                continue

            image_viewer.reset()
            edge_detector.reset_total_objects()

            try:
                file_names = [
                    f for f in os.listdir(folder)
                    if os.path.isfile(os.path.join(folder, f))
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
                continue

            window["-FILE LIST-"].update(file_names)

            for file_name in file_names:
                file_path = os.path.join(folder, file_name)
                process_image(image_viewer, edge_detector, file_path, min_val, max_val, ui_vars)
                image_viewer.clear_image_in_image_viewer()
                edge_detector.update_total_objects()

            window["-OBJECTS-"].update(
              f"Total Number of Objects Detected from Images in Folder: {edge_detector.total_objects}"
            )

        elif event == "-FILE LIST-" and values["-FILE LIST-"]:
            try:
                image_viewer.clear_info()
                file_path = os.path.join(folder, values["-FILE LIST-"][0])
                process_image(
                    image_viewer,
                    edge_detector,
                    file_path,
                    int(values['-cannyMinValue-']),
                    int(values['-cannyMaxValue-']),
                    ui_vars
                )
                image_viewer.show_image(TEMP_IMAGE_FILE)
                display_transformations(image_viewer, edge_detector, ui_vars)
                window["-num_of_objects-"].update(
                    f"Total number of objects detected in selected image: {edge_detector.current_objects}"
                )
            except:
                pass

    image_viewer.cleanup_temp_files()
    window.close()

if __name__ == "__main__":
    main()



