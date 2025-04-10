"""Configuration settings and validation for the Canny Edge Detector application."""

import os
import sys
from typing import Tuple

class ConfigurationError(Exception):
    """Exception raised for configuration validation errors."""
    pass

def validate_directory(path: str, create: bool = True) -> str:
    """Validate and optionally create a directory.
    
    Args:
        path: Directory path to validate
        create: Whether to create the directory if it doesn't exist
        
    Returns:
        The validated directory path
        
    Raises:
        ConfigurationError: If the directory cannot be created or accessed
    """
    try:
        if not os.path.exists(path) and create:
            os.makedirs(path)
        elif not os.path.exists(path):
            raise ConfigurationError(f"Directory does not exist: {path}")
        elif not os.path.isdir(path):
            raise ConfigurationError(f"Path is not a directory: {path}")
        return path
    except Exception as e:
        raise ConfigurationError(f"Error validating directory {path}: {str(e)}")

def validate_kernel_size(size: Tuple[int, int]) -> Tuple[int, int]:
    """Validate a kernel size tuple.
    
    Args:
        size: Tuple of (width, height) for the kernel
        
    Returns:
        The validated kernel size tuple
        
    Raises:
        ConfigurationError: If the kernel size is invalid
    """
    if not isinstance(size, tuple) or len(size) != 2:
        raise ConfigurationError("Kernel size must be a tuple of two integers")
    if not all(isinstance(x, int) and x > 0 and x % 2 == 1 for x in size):
        raise ConfigurationError("Kernel dimensions must be positive odd integers")
    return size

def validate_window_size(size: Tuple[int, int]) -> Tuple[int, int]:
    """Validate window size tuple.
    
    Args:
        size: Tuple of (width, height) for the window
        
    Returns:
        The validated window size tuple
        
    Raises:
        ConfigurationError: If the window size is invalid
    """
    if not isinstance(size, tuple) or len(size) != 2:
        raise ConfigurationError("Window size must be a tuple of two integers")
    if not all(isinstance(x, int) and x > 0 for x in size):
        raise ConfigurationError("Window dimensions must be positive integers")
    return size

# Directory Configuration
CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIRECTORY = validate_directory(os.path.join(CURRENT_DIRECTORY, 'src'))
ASSETS_DIRECTORY = validate_directory(os.path.join(CURRENT_DIRECTORY, 'assets'))
IMAGES_DIRECTORY = validate_directory(os.path.join(CURRENT_DIRECTORY, 'images'))
TEMP_DIRECTORY = validate_directory(os.path.join(CURRENT_DIRECTORY, 'temp'))

# UI Configuration
UI_THEME = 'DarkGrey8'
UI_FONT = ("Arial", 12)
WINDOW_SIZE = validate_window_size((1500, 710))

# Image Processing Configuration
SUPPORTED_FORMATS = ('.gif', '.jpg', '.png', '.pcx', '.bmp')
GAUSSIAN_KERNEL_SIZE = validate_kernel_size((5, 5))
GAUSSIAN_SIGMA = 0
DILATION_KERNEL_SIZE = validate_kernel_size((3, 3))
DEFAULT_MIN_THRESHOLD = 0
DEFAULT_MAX_THRESHOLD = 70

# Temporary Files
TEMP_IMAGE_FILE = os.path.join(TEMP_DIRECTORY, 'tmp.png')
TRANSFORM_IMAGE_FILE = os.path.join(TEMP_DIRECTORY, 'transformation.png')