"""Configuration settings for the Canny Edge Detector application."""

import os
from .base_config import (
    CURRENT_DIRECTORY,
    SRC_DIRECTORY,
    ASSETS_DIRECTORY,
    IMAGES_DIRECTORY,
    TEMP_DIRECTORY
)
from .services.configuration_service import ConfigurationService

# UI Configuration
UI_THEME = 'DarkGrey8'
UI_FONT = ("Arial", 12)
WINDOW_SIZE = (1750, 800)

# Image Processing Configuration
SUPPORTED_FORMATS = ('.gif', '.jpg', '.png', '.pcx', '.bmp')
GAUSSIAN_KERNEL_SIZE = (5, 5)
GAUSSIAN_SIGMA = 0
DILATION_KERNEL_SIZE = (3, 3)
DEFAULT_MIN_THRESHOLD = 0
DEFAULT_MAX_THRESHOLD = 70

# Temporary Files
TEMP_IMAGE_FILE = os.path.join(TEMP_DIRECTORY, 'tmp.png')
TRANSFORM_IMAGE_FILE = os.path.join(TEMP_DIRECTORY, 'transformation.png')
EMPTY_IMAGE_PATH = os.path.join(ASSETS_DIRECTORY, 'empty.png')

# Validate configuration
config_service = ConfigurationService()
config_service.validate_directory(SRC_DIRECTORY)
config_service.validate_directory(ASSETS_DIRECTORY)
config_service.validate_directory(IMAGES_DIRECTORY)
config_service.validate_directory(TEMP_DIRECTORY)
config_service.validate_window_size(WINDOW_SIZE)
config_service.validate_kernel_size(GAUSSIAN_KERNEL_SIZE)
config_service.validate_kernel_size(DILATION_KERNEL_SIZE)