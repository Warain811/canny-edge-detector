"""Main module for the Canny Edge Detection application."""

import os
import cv2
import numpy as np
import PySimpleGUI as sg

from src.open_image import ImageViewer
from src.canny_edge_detector import EdgeDetector
from src.name_convention import UIVariables
from src.config import (
    CURRENT_DIRECTORY,
    ASSETS_DIRECTORY,
    SUPPORTED_FORMATS,
    UI_THEME,
    UI_FONT,
    WINDOW_SIZE,
    DEFAULT_MIN_THRESHOLD,
    DEFAULT_MAX_THRESHOLD,
    TEMP_IMAGE_FILE,
    TRANSFORM_IMAGE_FILE
)

def create_directory_structure():
    """Create necessary directories if they don't exist."""
    for directory in [ASSETS_DIRECTORY]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def create_folder_column(ui_vars):
    """Create the left column containing folder selection and controls."""
    return [
        [
            sg.Text("Folder Path:", text_color="yellow"),
            sg.Input(size=(26, 1), disabled=True, text_color="black", key="-FOLDER-"),
            sg.Button('Browse'),
            sg.Button("Load Images\n and Detect Objects", size=(18, 2)),
        ],
        [
            sg.Text(
                "Images Found From Folder:",
                size=(60, 1),
                text_color="yellow",
                justification='center'
            )
        ],
        [
            sg.Listbox(
                values=[],
                enable_events=True,
                size=(55, 7),
                key="-FILE LIST-",
                horizontal_scroll=True
            ),
        ],
        [
            sg.Text(
                "Total Number of Objects Detected from Images in Folder: ",
                size=(60, 1),
                key='-OBJECTS-',
                text_color="yellow",
                justification='center'
            ),
        ],
        [
            sg.Text(
                "Hysteresis Threshold Values: ",
                size=(40, 1),
                text_color="white",
                justification='center',
                p=((0, 0), (30, 0))
            ),
        ],
        [
            sg.Text(
                "Min Value: ",
                size=(60, 1),
                text_color="yellow",
                justification='center',
                p=((0, 0), (0, 5))
            )
        ],
        [
            sg.Slider(
                range=(0, 255),
                default_value=DEFAULT_MIN_THRESHOLD,
                orientation='h',
                size=(30, 20),
                key="-cannyMinValue-"
            )
        ],
        [
            sg.Text(
                "Max Value: ",
                size=(60, 1),
                text_color="yellow",
                justification='center',
                p=((0, 0), (0, 5))
            )
        ],
        [
            sg.Slider(
                range=(0, 255),
                default_value=DEFAULT_MAX_THRESHOLD,
                orientation='h',
                size=(30, 20),
                key="-cannyMaxValue-"
            )
        ]
    ]

def create_image_viewer_column():
    """Create the center column containing the main image view."""
    return [
        [sg.Text("View of the image:", text_color="yellow", justification='center')],
        [
            sg.Image(
                key="-IMAGE-",
                size=(320, 240),
                filename=os.path.join(CURRENT_DIRECTORY, 'assets', 'empty.png')
            ),
        ],
    ]

def create_transformation_column(ui_vars):
    """Create the right column containing transformation views."""
    return [
        [
            sg.Text(
                size=(60, 2),
                key=ui_vars.first_transformation,
                text_color="yellow",
                justification='center'
            )
        ],
        [
            sg.Image(
                key=ui_vars.blur_image,
                size=(320, 240),
                pad=((0, 10), (0, 25))
            ),
            sg.Image(
                key=ui_vars.edges_image,
                size=(320, 240),
                pad=((0, 0), (0, 25))
            ),
        ],
        [
            sg.Text(
                size=(60, 2),
                key=ui_vars.second_transformation,
                text_color="yellow",
                justification='center'
            )
        ],
        [
            sg.Image(
                key=ui_vars.dilated_edges_image,
                size=(320, 240)
            ),
            sg.Image(
                key=ui_vars.contours_image,
                size=(320, 240)
            ),
        ],
        [
            sg.Text(
                size=(60, 1),
                key="-num_of_objects-",
                text_color="yellow",
                justification='center'
            )
        ],
    ]

def create_window():
    """Create and configure the main application window."""
    sg.theme(UI_THEME)
    ui_vars = UIVariables()

    layout = [
        [
            sg.Column(
                create_folder_column(ui_vars),
                vertical_alignment='center',
                element_justification='center',
                p=((0, 3), (60, 75))
            ),
            sg.VSeperator(),
            sg.Column(
                create_image_viewer_column(),
                element_justification="center",
                expand_y=True
            ),
            sg.VSeperator(),
            sg.Column(
                create_transformation_column(ui_vars),
                element_justification="center",
                expand_y=True
            ),
        ]
    ]

    return sg.Window(
        "Object Detection through Canny Algorithm",
        layout,
        font=UI_FONT,
        resizable=True,
        finalize=True,
        size=WINDOW_SIZE
    )

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



