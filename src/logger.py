"""Logging configuration for the Canny Edge Detector application."""

import logging
import os
from datetime import datetime
from .base_config import LOGS_DIRECTORY

def setup_logger():
    """Configure and return the application logger."""
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)

    # Configure logging
    log_file = os.path.join(
        LOGS_DIRECTORY,
        f'canny_edge_detector_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    
    logger = logging.getLogger('CannyEdgeDetector')
    logger.setLevel(logging.INFO)

    # File handler with UTF-8 encoding
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    
    # Console handler with ASCII-only output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    # Format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

# Create and configure the logger
logger = setup_logger()