"""Service for handling image format conversions."""

import os
from PIL import Image, UnidentifiedImageError
from ..pcx_handler import PCXHandler
from ..logger import logger

class ImageConversionService:
    """Service for handling image format conversion operations."""

    @staticmethod
    def convert_to_png(image_path: str, output_path: str):
        """Convert any supported image format to PNG.
        
        Args:
            image_path: Path to the source image file
            output_path: Path where the PNG should be saved
        
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
                ImageConversionService._convert_png(image_path, output_path)
            elif not file_name.lower().endswith('.pcx'):
                ImageConversionService._convert_standard_image(image_path, output_path)
            else:
                ImageConversionService._convert_pcx(image_path, output_path)
            logger.debug(f"Successfully converted {image_path} to PNG")
        except Exception as e:
            logger.error(f"Error converting image {image_path}: {str(e)}")
            raise

    @staticmethod
    def _convert_png(image_path: str, output_path: str):
        """Handle transparent PNG conversion."""
        try:
            png = Image.open(image_path).convert('RGBA')
            png.load()
            background = Image.new("RGB", png.size, (255, 255, 255))
            background.paste(png, mask=png.split()[3])
            background.save(output_path, 'PNG')
        except Exception as e:
            logger.error(f"Error converting PNG {image_path}: {str(e)}")
            raise

    @staticmethod
    def _convert_standard_image(image_path: str, output_path: str):
        """Convert standard image formats to RGB PNG."""
        try:
            image = Image.open(image_path)
            rgb_image = image.convert("RGB")
            rgb_image.save(output_path)
        except UnidentifiedImageError:
            logger.error(f"Unsupported image format: {image_path}")
            raise
        except Exception as e:
            logger.error(f"Error converting standard image {image_path}: {str(e)}")
            raise

    @staticmethod
    def _convert_pcx(image_path: str, output_path: str):
        """Convert PCX format to PNG."""
        try:
            image_data = PCXHandler.convert_pcx(image_path)
            image_data.save(output_path)
        except Exception as e:
            logger.error(f"Error converting PCX {image_path}: {str(e)}")
            raise

    @staticmethod
    def create_blank_image(width: int, height: int, output_path: str):
        """Create a blank transparent PNG image.
        
        Args:
            width: Width of the image in pixels
            height: Height of the image in pixels
            output_path: Path where the PNG should be saved
        """
        try:
            blank = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            blank.save(output_path, "PNG")
        except Exception as e:
            logger.error(f"Error creating blank image: {str(e)}")
            raise

    @staticmethod
    def resize_image(image_path: str, output_path: str, max_width: int, max_height: int):
        """Resize an image while maintaining aspect ratio.
        
        Args:
            image_path: Path to the source image
            output_path: Path where the resized image should be saved
            max_width: Maximum width of the output image
            max_height: Maximum height of the output image
        """
        try:
            # Load original image
            image = Image.open(image_path)

            # Resize while maintaining aspect ratio
            image.thumbnail((max_width, max_height), Image.LANCZOS)
            resized_width, resized_height = image.size

            # Create padded canvas
            padded_image = Image.new("RGBA", (max_width, max_height), (0, 0, 0, 0))

            # Center the image
            offset_x = (max_width - resized_width) // 2
            offset_y = (max_height - resized_height) // 2
            padded_image.paste(image, (offset_x, offset_y))

            # Save to file
            padded_image.save(output_path, "PNG")

        except Exception as e:
            logger.error(f"Error resizing image {image_path}: {str(e)}")
            raise