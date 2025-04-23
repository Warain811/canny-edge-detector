"""Module containing UI layout and window creation logic."""

import PySimpleGUI as sg

from .ui_config import (
    UI_THEME,
    UI_FONT,
    WINDOW_SIZE,
    EMPTY_IMAGE_PATH
)
from ...config.processing_config import (
    DEFAULT_MIN_THRESHOLD,
    DEFAULT_MAX_THRESHOLD
)
from .ui_variables import UIVariables

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
                filename=EMPTY_IMAGE_PATH
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