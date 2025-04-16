"""Service for handling PCX image format conversion with accurate pixel processing."""

import io
from PIL import Image
from .logger import logger

class PCXFormatError(Exception):
    """Exception raised for errors in PCX file format."""
    pass

class PCXService:
    """Handles PCX image processing using Pillow for dimensions and custom RLE decoding."""
    
    @staticmethod
    def convert_pcx(file_path, extract_palette=False):
        """Converts a PCX file with accurate dimensions from Pillow and custom pixel decoding.
        
        Args:
            file_path (str): Path to the PCX file
            extract_palette (bool): Whether to extract color palette
            
        Returns:
            tuple: (PIL.Image, list) if extract_palette=True
                  PIL.Image if extract_palette=False
                  
        Raises:
            PCXFormatError: If the file is invalid
        """
        logger.info(f"Processing PCX file: {file_path}")
        
        try:
            # Get dimensions from Pillow (but don't trust its pixel data)
            with Image.open(file_path) as pil_img:
                width, height = pil_img.size
            
            # Process file manually for accurate data
            with open(file_path, 'rb') as f:
                byte_data = bytearray(f.read())
                
                # Extract color palette (last 768 bytes)
                if len(byte_data) < 768:
                    raise PCXFormatError("File too small to contain PCX palette")
                
                palette_bytes = byte_data[-768:]
                color_palette = [
                    (palette_bytes[i], palette_bytes[i+1], palette_bytes[i+2])
                    for i in range(0, 768, 3)
                ]
                
                # Process RLE data
                position = 128  # Skip header
                decoded_pixels = []
                
                while position < len(byte_data) - 768:
                    byte = byte_data[position]
                    position += 1

                    if (byte & 0xC0) == 0xC0:
                        # RLE compressed sequence
                        run_length = byte & 0x3F
                        if position >= len(byte_data) - 768:
                            break
                        run_value = byte_data[position]
                        position += 1
                        decoded_pixels.extend([run_value] * run_length)
                    else:
                        # Single pixel
                        decoded_pixels.append(byte)
                
                # Verify pixel count matches dimensions
                expected_pixels = width * height
                if len(decoded_pixels) < expected_pixels:
                    raise PCXFormatError(f"Insufficient pixel data (got {len(decoded_pixels)}, need {expected_pixels})")
                
                # Create image using correct dimensions and custom data
                img = Image.new('P', (width, height))
                img.putpalette([c for rgb in color_palette for c in rgb])
                img.putdata(decoded_pixels[:expected_pixels])
                
                logger.info(f"Created {width}x{height} image with custom decoding")
                rgb_img = img.convert('RGB')
                
                return (rgb_img, color_palette) if extract_palette else rgb_img
                
        except Exception as e:
            logger.error(f"PCX processing failed: {str(e)}")
            raise PCXFormatError(f"Invalid PCX file: {str(e)}")
