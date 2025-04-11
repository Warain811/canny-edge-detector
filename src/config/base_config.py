"""Base configuration settings that don't require other module dependencies."""

import os

# Directory Configuration
CURRENT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directory Paths
SRC_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'src')
ASSETS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'assets')
IMAGES_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'images')
TEMP_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'temp')
LOGS_DIRECTORY = os.path.join(CURRENT_DIRECTORY, 'logs')