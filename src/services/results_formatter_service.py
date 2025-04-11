"""Service for formatting and standardizing UI result displays."""

from ..models.image_model import ImageModel
from ..models.image_transformation import ImageTransformation
from ..logger import logger

class ResultsFormatterService:
    """Service for formatting display results consistently."""

    @staticmethod
    def format_object_count(count: int, is_total: bool = False) -> str:
        """Format the object count display string.
        
        Args:
            count: Number of objects to display
            is_total: Whether this is a total count across all images
            
        Returns:
            Formatted string for display
        """
        if is_total:
            return f"Total Number of Objects Detected from Images in Folder: {count}"
        return f"Total number of objects detected in selected image: {count}"

    @staticmethod
    def format_transformation_description(transformation_type: str) -> str:
        """Format the transformation step description.
        
        Args:
            transformation_type: Type of transformation being displayed
            
        Returns:
            Formatted description string
        """
        descriptions = {
            "edge_detection": (
                "Gaussian Blurred, Grayscaled Image, \n"
                "and Edges Detected through Canny Algorithm (left to right):"
            ),
            "contour_detection": (
                "Dilated Edges, \n"
                "and External Contours Filled (left to right):"
            ),
            "processing": "",  # Empty string for intermediate steps
        }
        return descriptions.get(transformation_type, "")

    @staticmethod
    def format_threshold_values(min_val: int, max_val: int) -> str:
        """Format the threshold values for display.
        
        Args:
            min_val: Minimum threshold value
            max_val: Maximum threshold value
            
        Returns:
            Formatted threshold string
        """
        return f"Min: {min_val}, Max: {max_val}"

    @staticmethod
    def format_error_message(error: Exception, severity: str = "Error") -> str:
        """Format error messages consistently.
        
        Args:
            error: The exception to format
            severity: Error severity level
            
        Returns:
            Formatted error message
        """
        error_type = error.__class__.__name__
        message = str(error)
        return f"{severity}: {error_type} - {message}"