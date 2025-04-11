"""Service for handling UI update operations."""

import io
from PIL import Image, ImageTk
from ..name_convention import UIVariables
from ..services.image_conversion_service import ImageConversionService
from ..logger import logger
from ..config import TRANSFORM_IMAGE_FILE

class UIUpdateService:
    """Service for handling UI update operations."""

    def __init__(self, window):
        """Initialize the UI update service.
        
        Args:
            window: PySimpleGUI window instance
        """
        self.window = window
        self.ui_vars = UIVariables()
        self.image_converter = ImageConversionService()
        self._photo_images = {}  # Store PhotoImage references

    def update_file_list(self, files):
        """Update the file list in the UI.
        
        Args:
            files: List of filenames to display
        """
        self.window["-FILE LIST-"].update(files)

    def update_object_count(self, count: int, is_total: bool = False):
        """Update the object count display.
        
        Args:
            count: Number of objects to display
            is_total: Whether this is the total count across all images
        """
        if is_total:
            self.window["-OBJECTS-"].update(
                f"Total Number of Objects Detected from Images in Folder: {count}"
            )
        else:
            self.window["-num_of_objects-"].update(
                f"Total number of objects detected in selected image: {count}"
            )

    def show_image(self, file_path: str, is_main: bool = True):
        """Display an image in the UI.
        
        Args:
            file_path: Path to the image file
            is_main: Whether to show in main viewer (True) or transformation area (False)
        """
        try:
            logger.debug(f"Displaying image: {file_path}")
            image = Image.open(file_path)
            
            if is_main:
                bio = io.BytesIO()
                image.save(bio, "PNG")
                self.window["-IMAGE-"].update(data=bio.getvalue())
            else:
                self.window["-IMAGE-"].update(filename=file_path)
                
        except Exception as e:
            logger.error(f"Error displaying image {file_path}: {str(e)}")
            raise

    def show_transformation(self, transform_name: str, transform_image: str, description: str):
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

    def clear_transformations(self):
        """Clear all transformation displays."""
        logger.debug("Clearing transformation displays")
        self._photo_images.clear()  # Clear photo references
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

    def update_folder_path(self, path: str):
        """Update the folder path display.
        
        Args:
            path: Path to display
        """
        self.window['-FOLDER-'].update(path)

    def reset_state(self):
        """Reset all UI elements to their initial state."""
        logger.info("Resetting UI state")
        self.clear_transformations()
        self.window["-FILE LIST-"].update('')