"""Module for handling image loading, conversion, and display."""

import io
import os
from os.path import exists
from PIL import Image, ImageTk, UnidentifiedImageError

from .config import TEMP_IMAGE_FILE, TRANSFORM_IMAGE_FILE
from .name_convention import UIVariables
from .pcx_handler import PCXHandler
from .logger import logger

class ImageViewer:
    """Handles image loading, conversion, and display in the UI."""
    
    def __init__(self, window):
        """Initialize ImageViewer with a window reference.
        
        Args:
            window: PySimpleGUI window instance
        """
        self.window = window
        self.ui_variables = UIVariables()
        self.current_image = ""
        self.file_list = []
        self.temporary_files = [TEMP_IMAGE_FILE, TRANSFORM_IMAGE_FILE]
        logger.info("ImageViewer initialized")

    def convert_to_png(self, image_path):
        """Convert any supported image format to PNG.
        
        Args:
            image_path (str): Path to the image file
        
        Raises:
            FileNotFoundError: If the image file doesn't exist
            UnidentifiedImageError: If the image format is not supported
            IOError: If there's an error reading or writing the image
        """
        if not os.path.exists(image_path):
            logger.error(f"Image file not found: {image_path}")
            raise FileNotFoundError(f"Image file not found: {image_path}")

        logger.info(f"Converting image to PNG: {image_path}")
        file_name = os.path.basename(image_path)
        
        try:
            if file_name.lower().endswith('.png'):
                self._convert_png(image_path)
            elif not file_name.lower().endswith('.pcx'):
                self._convert_standard_image(image_path)
            else:
                self._convert_pcx(image_path)
            logger.debug(f"Successfully converted {image_path} to PNG")
        except Exception as e:
            logger.error(f"Error converting image {image_path}: {str(e)}")
            raise

    def _convert_png(self, image_path):
        """Handle transparent PNG conversion."""
        try:
            png = Image.open(image_path).convert('RGBA')
            png.load()
            background = Image.new("RGB", png.size, (255, 255, 255))
            background.paste(png, mask=png.split()[3])
            background.save(TEMP_IMAGE_FILE, 'PNG')
        except Exception as e:
            logger.error(f"Error converting PNG {image_path}: {str(e)}")
            raise

    def _convert_standard_image(self, image_path):
        """Convert standard image formats to RGB PNG."""
        try:
            image = Image.open(image_path)
            rgb_image = image.convert("RGB")
            rgb_image.save(TEMP_IMAGE_FILE)
        except UnidentifiedImageError:
            logger.error(f"Unsupported image format: {image_path}")
            raise
        except Exception as e:
            logger.error(f"Error converting standard image {image_path}: {str(e)}")
            raise

    def _convert_pcx(self, image_path):
        """Convert PCX format to PNG."""
        try:
            image_data = PCXHandler.convert_pcx(image_path)
            image_data.save(TEMP_IMAGE_FILE)
        except Exception as e:
            logger.error(f"Error converting PCX {image_path}: {str(e)}")
            raise

    def clear_info(self):
        """Clear all transformation displays."""
        logger.debug("Clearing transformation displays")
        for key in [
            self.ui_variables.first_transformation,
            self.ui_variables.second_transformation,
            self.ui_variables.blur_image,
            self.ui_variables.edges_image,
            self.ui_variables.dilated_edges_image,
            self.ui_variables.contours_image,
            "-num_of_objects-"
        ]:
            self.window[key].update('')
    
    def clear_image_in_image_viewer(self):
        """Clear the image displayed in the viewer."""
        try:
            logger.debug("Clearing main image viewer")

            # Load and scale the image proportionally
            empty_image = Image.open("assets/empty.png")
            empty_image.thumbnail((320, 240))  # Maintains aspect ratio

            # Create a new image with padding (a fixed 320x240 blank canvas)
            padded_image = Image.new("RGBA", (320, 240), (0, 0, 0, 0))  # Transparent background

            # Calculate top-left corner for centering
            x = (320 - empty_image.width) // 2
            y = (240 - empty_image.height) // 2

            # Paste the thumbnail into the center of the canvas
            padded_image.paste(empty_image, (x, y))

            # Convert to bytes and update
            bio = io.BytesIO()
            padded_image.save(bio, "PNG")
            self.window["-IMAGE-"].update(data=bio.getvalue())

        except Exception as e:
            logger.error(f"Error clearing image viewer: {str(e)}")
            raise

    def reset(self):
        """Reset the viewer state."""
        logger.info("Resetting viewer state")
        self.clear_info()
        self.window["-FILE LIST-"].update('')

    def show_transformation(self, transform_name, transform_image, description):
        """Display a transformation step in the UI.
        
        Args:
            transform_name (str): Key for the transformation description
            transform_image (str): Key for the transformation image
            description (str): Description of the transformation
        """
        try:
            logger.debug(f"Showing transformation: {transform_name}")
            image = Image.open(TRANSFORM_IMAGE_FILE)
            image.thumbnail((320, 240))  # Updated to match the size in create_image_viewer_column
            self.window[transform_name].update(description)
            self.window[transform_image].update(data=ImageTk.PhotoImage(image))
        except Exception as e:
            logger.error(f"Error showing transformation {transform_name}: {str(e)}")
            raise

    def cleanup_temp_files(self):
        """Remove temporary image files."""
        logger.debug("Cleaning up temporary files")
        for file_name in self.temporary_files:
            if exists(file_name):
                try:
                    os.remove(file_name)
                    logger.debug(f"Removed temporary file: {file_name}")
                except Exception as e:
                    logger.warning(f"Failed to remove temporary file {file_name}: {str(e)}")

    def show_image(self, file_path):
        """Display the main image in the UI.
        
        Args:
            file_path (str): Path to the image file
        """
        try:
            logger.debug(f"Displaying image: {file_path}")
            image = Image.open(file_path)
            image.thumbnail((320, 240))  # Updated to match the size in create_image_viewer_column
            bio = io.BytesIO()
            image.save(bio, "PNG")
            self.window["-IMAGE-"].update(data=bio.getvalue())
        except Exception as e:
            logger.error(f"Error displaying image {file_path}: {str(e)}")
            raise

