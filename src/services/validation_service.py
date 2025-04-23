"""Service for handling input validation and error messages."""

import PySimpleGUI as sg
from ..ui.ui_config import UI_FONT

class ValidationService:
    """Service for handling input validation and error messages."""

    @staticmethod
    def validate_folder_selection(folder_path: str) -> bool:
        """Validate that a folder has been selected.
        
        Args:
            folder_path: Path to the selected folder
            
        Returns:
            True if validation passes, False otherwise
        """
        if not folder_path:
            ValidationService.show_error(
                "Please choose a nonempty folder. Program will use previously loaded folder."
            )
            return False
        return True

    @staticmethod
    def validate_threshold_values(min_val: int, max_val: int) -> bool:
        """Validate Canny edge detection threshold values.
        
        Args:
            min_val: Minimum threshold value
            max_val: Maximum threshold value
            
        Returns:
            True if validation passes, False otherwise
        """
        if min_val > max_val:
            ValidationService.show_error("Min value cannot exceed max value.")
            return False
        return True

    @staticmethod
    def validate_image_files(file_count: int) -> bool:
        """Validate that image files were found.
        
        Args:
            file_count: Number of image files found
            
        Returns:
            True if validation passes, False otherwise
        """
        if file_count == 0:
            ValidationService.show_error(
                "Chosen folder is empty. Please choose a different folder",
                severity="Warning"
            )
            return False
        return True

    @staticmethod
    def show_error(message: str, severity: str = "Error") -> None:
        """Display an error message to the user.
        
        Args:
            message: The error message to display
            severity: The severity level of the error ("Error" or "Warning")
        """
        sg.Popup(
            message,
            font=UI_FONT,
            button_type=5,
            title=severity
        )