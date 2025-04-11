"""Main module for the Canny Edge Detection application."""

import os
from src.base_config import ASSETS_DIRECTORY
from src.presentation.ui.layout import create_window
from src.presentation.ui.event_controller import EventController

def create_directory_structure():
    """Create necessary directories if they don't exist."""
    for directory in [ASSETS_DIRECTORY]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def main():
    """Main application entry point."""
    create_directory_structure()
    window = create_window()
    controller = EventController(window)

    while True:
        event, values = window.read()
        if not controller.handle_event(event, values):
            break

    controller.cleanup()

if __name__ == "__main__":
    main()



