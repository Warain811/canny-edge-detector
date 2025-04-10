"""Logging configuration for the Canny Edge Detector application."""

import logging
import os
from datetime import datetime
from .config import CURRENT_DIRECTORY

def setup_logger():
    """Configure and return the application logger."""
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(CURRENT_DIRECTORY, 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Configure logging
    log_file = os.path.join(
        logs_dir,
        f'canny_edge_detector_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    )
    
    logger = logging.getLogger('CannyEdgeDetector')
    logger.setLevel(logging.INFO)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)
    
    # Console handler
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