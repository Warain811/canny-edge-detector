"""Service for handling image processing operations."""

import cv2
import numpy as np
from ..config.processing_config import (
    GAUSSIAN_KERNEL_SIZE,
    GAUSSIAN_SIGMA,
    DILATION_KERNEL_SIZE
)
from ..models.image_model import ImageModel
from ..models.image_transformation import ImageTransformation

class ImageProcessingService:
    """Service for handling image processing operations."""

    def __init__(self):
        """Initialize the image processing service."""
        self._current_transformation = None
        self._total_objects = 0

    @property
    def current_objects(self) -> int:
        """Get the number of objects in current image."""
        return self._current_transformation.result.object_count if self._current_transformation else 0

    @property
    def total_objects(self) -> int:
        """Get total number of objects detected."""
        return self._total_objects

    @property
    def image(self) -> np.ndarray:
        """Get the current image data."""
        return self._current_transformation.result.data if self._current_transformation else None

    @property
    def blurred_image(self) -> np.ndarray:
        """Get the blurred image data."""
        return self._current_transformation.result.blurred if self._current_transformation else None

    @property
    def edges(self) -> np.ndarray:
        """Get the detected edges."""
        return self._current_transformation.result.edges if self._current_transformation else None

    @property
    def dilated_edges(self) -> np.ndarray:
        """Get the dilated edges."""
        return self._current_transformation.result.dilated_edges if self._current_transformation else None

    @property
    def contours(self) -> list:
        """Get the detected contours."""
        return self._current_transformation.result.contours if self._current_transformation else None

    def process_image(self, filepath: str, min_threshold: int, max_threshold: int):
        """Process an image through the edge detection pipeline."""
        try:
            # Load and create initial image model
            image_data = cv2.imread(filepath)
            if image_data is None:
                raise IOError(f"Failed to load image: {filepath}")
            
            height, width = image_data.shape[:2]
            original_image = ImageModel(
                path=filepath,
                data=image_data,
                width=width,
                height=height,
                format=filepath.split('.')[-1].lower()
            )
            
            # Create transformation model
            self._current_transformation = ImageTransformation(
                original_image=original_image,
                min_threshold=min_threshold,
                max_threshold=max_threshold,
                gaussian_kernel_size=GAUSSIAN_KERNEL_SIZE,
                gaussian_sigma=GAUSSIAN_SIGMA,
                dilation_kernel_size=DILATION_KERNEL_SIZE
            )
            
            if not self._current_transformation.is_valid():
                raise ValueError("Invalid threshold values")

            # Process the image
            self._preprocess_image()
            self._detect_edges()
            self._detect_contours()
            
        except Exception as e:
            raise

    def _preprocess_image(self):
        """Convert image to grayscale and apply Gaussian blur."""
        try:
            # Create result model if not exists
            if not self._current_transformation.result:
                self._current_transformation.result = ImageModel(
                    path=self._current_transformation.original_image.path,
                    data=self._current_transformation.original_image.data.copy(),
                    width=self._current_transformation.original_image.width,
                    height=self._current_transformation.original_image.height,
                    format=self._current_transformation.original_image.format
                )
            
            # Apply transformations
            gray_image = cv2.cvtColor(self._current_transformation.result.data, cv2.COLOR_BGR2GRAY)
            self._current_transformation.result.grayscale = gray_image
            
            self._current_transformation.result.blurred = cv2.GaussianBlur(
                gray_image, 
                self._current_transformation.gaussian_kernel_size, 
                self._current_transformation.gaussian_sigma
            )
        except Exception as e:
            raise

    def _detect_edges(self):
        """Apply Canny edge detection algorithm."""
        try:
            self._current_transformation.result.edges = cv2.Canny(
                self._current_transformation.result.blurred,
                self._current_transformation.min_threshold,
                self._current_transformation.max_threshold,
                L2gradient=True,
                apertureSize=3
            )
            
            self._current_transformation.result.dilated_edges = cv2.blur(
                self._current_transformation.result.edges, 
                self._current_transformation.dilation_kernel_size, 
                0
            )
        except Exception as e:
            raise

    def _detect_contours(self):
        """Find external contours in the image."""
        try:
            contours, _ = cv2.findContours(
                self._current_transformation.result.dilated_edges.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            self._current_transformation.result.contours = contours
            self._current_transformation.result.object_count = len(contours)
        except Exception as e:
            raise

    def update_total_objects(self):
        """Update the total count of objects across all processed images."""
        if self._current_transformation and self._current_transformation.result:
            self._total_objects += self._current_transformation.result.object_count

    def reset_total_objects(self):
        """Reset the total object count when loading a new folder."""
        self._total_objects = 0