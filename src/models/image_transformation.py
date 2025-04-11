"""Domain model for representing image transformations."""

from dataclasses import dataclass
from typing import Optional
import numpy as np
from .image_model import ImageModel

@dataclass
class ImageTransformation:
    """Represents a sequence of image transformations."""

    original_image: ImageModel
    min_threshold: int
    max_threshold: int
    
    # Processing parameters
    gaussian_kernel_size: tuple[int, int]
    gaussian_sigma: float
    dilation_kernel_size: tuple[int, int]
    
    # Results at each step
    result: Optional[ImageModel] = None
    
    def is_valid(self) -> bool:
        """Validate transformation parameters."""
        if not isinstance(self.min_threshold, (int, float)) or not isinstance(self.max_threshold, (int, float)):
            return False
        if self.min_threshold < 0 or self.max_threshold < 0:
            return False
        if self.min_threshold >= self.max_threshold:
            return False
        return True
    
    @property
    def is_complete(self) -> bool:
        """Check if all transformations have been applied."""
        return (self.result is not None and 
                self.result.has_edges and 
                self.result.has_contours)