"""Service for handling PCX image format conversion."""

import io
from PIL import Image
from ..logger import logger

class PCXFormatError(Exception):
    """Exception raised for errors in PCX file format."""
    pass

class PCXService:
    """Handles PCX image file format conversion and processing."""
    
    @staticmethod
    def convert_pcx(file_path):
        """Converts a PCX file to a PIL Image.
        
        Args:
            file_path (str): Path to the PCX file
            
        Returns:
            PIL.Image: Converted image in RGB format
            
        Raises:
            FileNotFoundError: If the PCX file doesn't exist
            PCXFormatError: If the file is not a valid PCX file
            IOError: If there's an error reading the file
        """
        logger.info(f"Converting PCX file: {file_path}")
        
        try:
            with open(file_path, 'rb') as f:
                # Read PCX header (128 bytes)
                manufacturer = int.from_bytes(f.read(1), byteorder='little')
                version = int.from_bytes(f.read(1), byteorder='little')
                encoding = int.from_bytes(f.read(1), byteorder='little')
                bits_per_pixel = int.from_bytes(f.read(1), byteorder='little')
                
                # Validate PCX format
                if manufacturer != 10:  # ZSoft manufacturer ID
                    raise PCXFormatError("Invalid manufacturer ID")
                if encoding != 1:  # RLE encoding
                    raise PCXFormatError("Unsupported encoding method")
                
                logger.debug(f"PCX version: {version}, bits per pixel: {bits_per_pixel}")
                
                # Read dimensions
                xmin = int.from_bytes(f.read(2), byteorder='little')
                ymin = int.from_bytes(f.read(2), byteorder='little')
                xmax = int.from_bytes(f.read(2), byteorder='little')
                ymax = int.from_bytes(f.read(2), byteorder='little')
                
                width = xmax - xmin + 1
                height = ymax - ymin + 1
                
                logger.debug(f"Image dimensions: {width}x{height}")
                
                if width <= 0 or height <= 0:
                    raise PCXFormatError("Invalid image dimensions")
                
                # Skip to image data
                f.seek(128)
                
                # Read and decode image data
                data = f.read()
                decoded_data = PCXService._decode_pcx_data(data, width, height)
                
                # Create image from decoded data
                image = Image.frombytes('RGB', (width, height), decoded_data)
                logger.info("PCX conversion completed successfully")
                return image
                
        except FileNotFoundError:
            logger.error(f"PCX file not found: {file_path}")
            raise
        except PCXFormatError as e:
            logger.error(f"Invalid PCX format in {file_path}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error converting PCX file {file_path}: {str(e)}")
            raise
    
    @staticmethod
    def _decode_pcx_data(data, width, height):
        """Decodes RLE-compressed PCX data.
        
        Args:
            data (bytes): Compressed PCX image data
            width (int): Image width
            height (int): Image height
            
        Returns:
            bytes: Decoded RGB image data
            
        Raises:
            PCXFormatError: If the compressed data is corrupted
        """
        try:
            decoded = bytearray()
            i = 0
            expected_size = width * height
            
            while i < len(data):
                if (data[i] & 0xC0) == 0xC0:  # RLE compression marker
                    count = data[i] & 0x3F
                    i += 1
                    if i >= len(data):
                        raise PCXFormatError("Unexpected end of compressed data")
                    value = data[i]
                    decoded.extend([value] * count)
                else:
                    decoded.append(data[i])
                i += 1
            
            if len(decoded) < expected_size:
                raise PCXFormatError("Insufficient decoded data")
            
            # Convert to RGB format
            rgb_data = bytearray()
            for pixel in range(0, expected_size):
                value = decoded[pixel]
                rgb_data.extend([value, value, value])  # Convert grayscale to RGB
            
            logger.debug(f"Decoded {len(decoded)} bytes to {len(rgb_data)} RGB bytes")
            return bytes(rgb_data)
            
        except IndexError:
            logger.error("Corrupted PCX data")
            raise PCXFormatError("Corrupted PCX data")
        except Exception as e:
            logger.error(f"Error decoding PCX data: {str(e)}")
            raise