"""Service for handling file management operations."""

import os
from typing import List
from .processing_config import SUPPORTED_FORMATS
from ..utils.logger import logger

class FileManagementService:
    """Service for handling file management operations."""

    @staticmethod
    def list_image_files(folder_path: str) -> List[str]:
        """List all supported image files in a folder.
        
        Args:
            folder_path: Path to the folder to search
            
        Returns:
            List of filenames that match supported formats
        """
        try:
            return [
                f for f in os.listdir(folder_path)
                if os.path.isfile(os.path.join(folder_path, f))
                and f.lower().endswith(SUPPORTED_FORMATS)
            ]
        except Exception as e:
            logger.error(f"Error listing files in {folder_path}: {str(e)}")
            return []

    @staticmethod
    def cleanup_files(file_paths: List[str]):
        """Remove specified files if they exist.
        
        Args:
            file_paths: List of file paths to remove
        """
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                    logger.debug(f"Removed file: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to remove file {file_path}: {str(e)}")

    @staticmethod
    def ensure_file_exists(file_path: str) -> bool:
        """Check if a file exists.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file exists, False otherwise
        """
        exists = os.path.exists(file_path)
        if not exists:
            logger.error(f"File not found: {file_path}")
        return exists