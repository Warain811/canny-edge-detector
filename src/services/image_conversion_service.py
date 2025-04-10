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
        """
        Resize an image to fit within a specified width and height, while maintaining its
        aspect ratio. If the image's aspect ratio doesn't match the target size, it will
        be centered on a transparent canvas of the specified size.

        Args:
            image_path (str): Path to the source image to resize.
            output_path (str): Path where the resized image will be saved.
            max_width (int): Maximum allowed width for the output image.
            max_height (int): Maximum allowed height for the output image.

        Returns:
            None: Saves the resized image to the output path.
        """
        try:
            # 1. Load the original image
            original_image = Image.open(image_path)

            # 2. Calculate the new size for the image, maintaining the aspect ratio
            resized_image = ImageConversionService._resize_image_to_max_dimensions(original_image, max_width, max_height)

            # 3. Create a canvas to center the resized image
            centered_image = ImageConversionService._create_centered_canvas(resized_image, max_width, max_height)

            # 4. Save the final image
            centered_image.save(output_path, "PNG")

            logger.info(f"✅ Resized image saved at {output_path}")

        except Exception as e:
            logger.error(f"Error resizing image from {image_path}: {str(e)}")
            raise
    
    @staticmethod
    def _resize_image_to_max_dimensions(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        """
        Resize an image while maintaining the aspect ratio, using LANCZOS for high-quality downscaling.
        
        Args:
            image (Image.Image): The image to resize.
            max_width (int): The maximum width for the resized image.
            max_height (int): The maximum height for the resized image.

        Returns:
            Image.Image: The resized image with maintained aspect ratio.
        """
        image.thumbnail((max_width, max_height), Image.LANCZOS)
        return image

    @staticmethod
    def _create_centered_canvas(image: Image.Image, canvas_width: int, canvas_height: int) -> Image.Image:
        """
        Create a canvas of the specified size, then center the image on that canvas.
        
        Args:
            image (Image.Image): The image to center.
            canvas_width (int): The width of the canvas.
            canvas_height (int): The height of the canvas.

        Returns:
            Image.Image: The image centered on the canvas.
        """
        canvas = Image.new("RGBA", (canvas_width, canvas_height), (0, 0, 0, 0))
        offset_x = (canvas_width - image.width) // 2
        offset_y = (canvas_height - image.height) // 2
        canvas.paste(image, (offset_x, offset_y))
        return canvas