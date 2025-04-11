"""Service for handling configuration validation."""

import os
from typing import Tuple
from ..logger import logger

class ConfigurationError(Exception):
    """Exception raised for configuration validation errors."""
    pass

class ConfigurationService:
    """Service for handling configuration validation."""

    @staticmethod
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
                logger.info(f"Created directory: {path}")
            elif not os.path.exists(path):
                raise ConfigurationError(f"Directory does not exist: {path}")
            elif not os.path.isdir(path):
                raise ConfigurationError(f"Path is not a directory: {path}")
            return path
        except Exception as e:
            logger.error(f"Error validating directory {path}: {str(e)}")
            raise ConfigurationError(f"Error validating directory {path}: {str(e)}")

    @staticmethod
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

    @staticmethod
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