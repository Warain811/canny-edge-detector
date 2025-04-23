"""UI-specific configuration settings."""

import os
from src.config.base_config import ASSETS_DIRECTORY

# UI Theme and Style
UI_THEME = 'DarkGrey8'
UI_FONT = ("Arial", 12)
WINDOW_SIZE = (1750, 800)

# UI Paths
EMPTY_IMAGE_PATH = os.path.join(ASSETS_DIRECTORY, 'empty.png')