"""Domain model for representing an image in the application."""

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class ImageModel:
    """Represents an image and its properties in the application."""
    
    path: str  # Path to the image file
    data: np.ndarray  # Image data as numpy array
    width: int
    height: int
    format: str  # Original image format (png, jpg, etc)
    
    # Optional properties for processed images
    grayscale: Optional[np.ndarray] = None  # Grayscale version of the image
    blurred: Optional[np.ndarray] = None  # Blurred version
    edges: Optional[np.ndarray] = None  # Detected edges
    dilated_edges: Optional[np.ndarray] = None  # Dilated edges
    contours: Optional[list] = None  # Detected contours
    object_count: int = 0  # Number of objects detected
    
    @property
    def size(self) -> tuple[int, int]:
        """Get the image dimensions."""
        return (self.width, self.height)
    
    @property
    def has_edges(self) -> bool:
        """Check if edge detection has been performed."""
        return self.edges is not None
    
    @property
    def has_contours(self) -> bool:
        """Check if contour detection has been performed."""
        return self.contours is not None