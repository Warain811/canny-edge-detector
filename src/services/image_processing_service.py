"""Service for handling all image processing operations."""

import cv2
import numpy as np
from ..config import (
    GAUSSIAN_KERNEL_SIZE,
    GAUSSIAN_SIGMA,
    DILATION_KERNEL_SIZE
)
from ..logger import logger

class ImageProcessingService:
    """Service for handling image processing operations."""

    def __init__(self):
        """Initialize the image processing service."""
        self._image = None
        self._blurred_image = None
        self._edges = None
        self._dilated_edges = None
        self._contours = None
        self._current_objects = 0

    @property
    def image(self):
        """Get the current image."""
        return self._image

    @property
    def blurred_image(self):
        """Get the blurred image."""
        return self._blurred_image

    @property
    def edges(self):
        """Get the detected edges."""
        return self._edges

    @property
    def dilated_edges(self):
        """Get the dilated edges."""
        return self._dilated_edges

    @property
    def contours(self):
        """Get the detected contours."""
        return self._contours

    @property
    def current_objects(self):
        """Get the number of objects in current image."""
        return self._current_objects

    def process_image(self, filepath: str, min_threshold: int, max_threshold: int):
        """Process an image through the edge detection pipeline.
        
        Args:
            filepath: Path to the image file
            min_threshold: Lower threshold for Canny edge detection
            max_threshold: Upper threshold for Canny edge detection
            
        Raises:
            IOError: If the image cannot be loaded
            ValueError: If thresholds are invalid
        """
        if not self._validate_thresholds(min_threshold, max_threshold):
            raise ValueError("Invalid threshold values")

        try:
            self._image = cv2.imread(filepath)
            if self._image is None:
                raise IOError(f"Failed to load image: {filepath}")
                
            logger.info(f"Processing image: {filepath}")
            logger.debug(f"Image shape: {self._image.shape}")
            
            self._preprocess_image()
            self._detect_edges(min_threshold, max_threshold)
            self._detect_contours()
            
            logger.info(f"Detected {self._current_objects} objects in image")
            
        except Exception as e:
            logger.error(f"Error processing image {filepath}: {str(e)}")
            raise

    def _preprocess_image(self):
        """Convert image to grayscale and apply Gaussian blur."""
        try:
            gray_image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
            self._blurred_image = cv2.GaussianBlur(
                gray_image, 
                GAUSSIAN_KERNEL_SIZE, 
                GAUSSIAN_SIGMA
            )
            logger.debug("Image preprocessing completed")
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise

    def _detect_edges(self, min_val: int, max_val: int):
        """Apply Canny edge detection algorithm."""
        try:
            logger.debug(f"Applying Canny with thresholds: {min_val}, {max_val}")
            self._edges = cv2.Canny(
                self._blurred_image,
                min_val,
                max_val,
                L2gradient=True,
                apertureSize=3
            )
            self._dilated_edges = cv2.blur(
                self._edges, 
                DILATION_KERNEL_SIZE, 
                0
            )
            logger.debug("Edge detection completed")
        except Exception as e:
            logger.error(f"Error in edge detection: {str(e)}")
            raise

    def _detect_contours(self):
        """Find external contours in the image."""
        try:
            contours, _ = cv2.findContours(
                self._dilated_edges.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            self._contours = contours
            self._current_objects = len(contours)
            logger.debug(f"Found {self._current_objects} contours")
        except Exception as e:
            logger.error(f"Error finding contours: {str(e)}")
            raise

    @staticmethod
    def _validate_thresholds(min_threshold: int, max_threshold: int) -> bool:
        """Validate Canny edge detection thresholds.
        
        Args:
            min_threshold: Lower threshold for the hysteresis procedure
            max_threshold: Upper threshold for the hysteresis procedure
            
        Returns:
            True if thresholds are valid, False otherwise
        """
        if not isinstance(min_threshold, (int, float)) or not isinstance(max_threshold, (int, float)):
            return False
        if min_threshold < 0 or max_threshold < 0:
            return False
        if min_threshold >= max_threshold:
            return False
        return True