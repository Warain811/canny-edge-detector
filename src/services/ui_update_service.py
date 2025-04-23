"""Service for handling UI update operations."""

import io
from PIL import Image, ImageTk
from ..presentation.ui.ui_variables import UIVariables
from .results_formatter_service import ResultsFormatterService

class UIUpdateService:
    """Service for handling UI update operations."""

    def __init__(self, window):
        """Initialize the UI update service.
        
        Args:
            window: PySimpleGUI window instance
        """
        self.window = window
        self.ui_vars = UIVariables()
        self._photo_images = {}  # Store PhotoImage references
        self._formatter = ResultsFormatterService()

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
        message = self._formatter.format_object_count(count, is_total)
        key = "-OBJECTS-" if is_total else "-num_of_objects-"
        self.window[key].update(message)

    def show_image(self, file_path: str, is_main: bool = True):
        """Display an image in the UI.
        
        Args:
            file_path: Path to the image file
            is_main: Whether to show in main viewer (True) or transformation area (False)
        """
        try:
            image = Image.open(file_path)
            
            if is_main:
                bio = io.BytesIO()
                image.save(bio, "PNG")
                self.window["-IMAGE-"].update(data=bio.getvalue())
            else:
                self.window["-IMAGE-"].update(filename=file_path)
                
        except Exception as e:
            pass

    def show_transformation(self, transform_name: str, transform_image: str, transformation_type: str):
        """Display a transformation step in the UI.
        
        Args:
            transform_name: Key for the transformation description
            transform_image: Key for the transformation image
            transformation_type: Type of transformation being displayed
        """
        try:
            image = Image.open(transform_image)
            photo = ImageTk.PhotoImage(image)
            self._photo_images[transform_image] = photo  # Keep reference
            
            description = self._formatter.format_transformation_description(transformation_type)
            self.window[transform_name].update(description)
            self.window[transform_image].update(data=photo)
            
        except Exception:
            pass

    def clear_transformations(self):
        """Clear all transformation displays."""
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
        self.clear_transformations()
        self.window["-FILE LIST-"].update('')