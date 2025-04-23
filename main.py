"""Main module for the Canny Edge Detection application."""

import os
from src.services.configuration_service import ConfigurationService
from src.presentation.ui.layout import create_window
from src.presentation.ui.event_controller import EventController
from src.config.base_config import ASSETS_DIRECTORY, TEMP_DIRECTORY

def create_directory_structure():
    """Create necessary directories if they don't exist."""
    config_service = ConfigurationService()
    for directory in [ASSETS_DIRECTORY, TEMP_DIRECTORY]:
        config_service.validate_directory(directory)

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



