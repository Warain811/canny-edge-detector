"""Configuration settings for image processing."""

import os
from ..base_config import TEMP_DIRECTORY

# Image Processing Parameters
GAUSSIAN_KERNEL_SIZE = (5, 5)
GAUSSIAN_SIGMA = 0
DILATION_KERNEL_SIZE = (3, 3)
DEFAULT_MIN_THRESHOLD = 0
DEFAULT_MAX_THRESHOLD = 70

# Supported Image Formats
SUPPORTED_FORMATS = ('.gif', '.jpg', '.png', '.pcx', '.bmp')

# Temporary Files
TEMP_IMAGE_FILE = os.path.join(TEMP_DIRECTORY, 'tmp.png')
TRANSFORM_IMAGE_FILE = os.path.join(TEMP_DIRECTORY, 'transformation.png')