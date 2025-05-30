"""Service for handling file management operations."""

import os
from typing import List

class FileManagementService:
    """Service for handling file management operations."""

    # Supported Image Formats
    SUPPORTED_FORMATS = ('.gif', '.jpg', '.png', '.pcx', '.bmp')

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
                and f.lower().endswith(FileManagementService.SUPPORTED_FORMATS)
            ]
        except Exception:
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
                except Exception:
                    pass

    @staticmethod
    def ensure_file_exists(file_path: str) -> bool:
        """Check if a file exists.
        
        Args:
            file_path: Path to the file to check
            
        Returns:
            True if the file exists, False otherwise
        """
        return os.path.exists(file_path)