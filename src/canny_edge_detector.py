"""Module for detecting edges and objects in images using the Canny algorithm."""

import cv2
import numpy as np
from .config import (
    GAUSSIAN_KERNEL_SIZE,
    GAUSSIAN_SIGMA,
    DILATION_KERNEL_SIZE
)
from .logger import logger

class EdgeDetector:
    """Handles edge detection and object counting using the Canny algorithm."""
    
    def __init__(self):
        self.image = []
        self.blurred_image = []
        self.edges = []
        self.dilated_edges = []
        self.contours = []
        self.total_objects = 0
        self.current_objects = 0
        logger.info("EdgeDetector initialized")

    @staticmethod
    def validate_thresholds(min_threshold, max_threshold):
        """Validates that the Canny edge detection thresholds are valid.
        
        Args:
            min_threshold (int): Lower threshold for the hysteresis procedure
            max_threshold (int): Upper threshold for the hysteresis procedure
            
        Returns:
            bool: True if thresholds are valid, False otherwise
        """
        if not isinstance(min_threshold, (int, float)) or not isinstance(max_threshold, (int, float)):
            return False
        if min_threshold < 0 or max_threshold < 0:
            return False
        if min_threshold >= max_threshold:
            return False
        return True

    def detect_edges(self, filepath, min_threshold, max_threshold):
        """Detects edges in an image using the Canny edge detection algorithm.
        
        Args:
            filepath (str): Path to the image file
            min_threshold (int): Lower threshold for the hysteresis procedure
            max_threshold (int): Upper threshold for the hysteresis procedure
        """
        try:
            self.image = cv2.imread(filepath)
            if self.image is None:
                raise IOError(f"Failed to load image: {filepath}")
                
            logger.info(f"Processing image: {filepath}")
            logger.debug(f"Image shape: {self.image.shape}")
            
            self._preprocess_image()
            self._detect_canny_edges(min_threshold, max_threshold)
            self._find_contours()
            
            logger.info(f"Detected {self.current_objects} objects in image")
            
        except Exception as e:
            logger.error(f"Error processing image {filepath}: {str(e)}")
            raise
    
    def _preprocess_image(self):
        """Convert image to grayscale and apply Gaussian blur."""
        try:
            gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.blurred_image = cv2.GaussianBlur(
                gray_image, 
                GAUSSIAN_KERNEL_SIZE, 
                GAUSSIAN_SIGMA
            )
            logger.debug("Image preprocessing completed")
        except Exception as e:
            logger.error(f"Error in preprocessing: {str(e)}")
            raise
    
    def _detect_canny_edges(self, min_val, max_val):
        """Apply Canny edge detection algorithm."""
        try:
            logger.debug(f"Applying Canny with thresholds: {min_val}, {max_val}")
            self.edges = cv2.Canny(
                self.blurred_image,
                min_val,
                max_val,
                L2gradient=True,
                apertureSize=3
            )
            self.dilated_edges = cv2.blur(
                self.edges, 
                DILATION_KERNEL_SIZE, 
                0
            )
            logger.debug("Edge detection completed")
        except Exception as e:
            logger.error(f"Error in edge detection: {str(e)}")
            raise
    
    def _find_contours(self):
        """Find external contours in the image."""
        try:
            contours, _ = cv2.findContours(
                self.dilated_edges.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            self.contours = contours
            self.current_objects = len(contours)
            logger.debug(f"Found {self.current_objects} contours")
        except Exception as e:
            logger.error(f"Error finding contours: {str(e)}")
            raise
    
    def update_total_objects(self):
        """Update the total count of objects across all processed images."""
        self.total_objects += self.current_objects
        logger.info(f"Total object count updated to: {self.total_objects}")
    
    def reset_total_objects(self):
        """Reset the total object count when loading a new folder."""
        self.total_objects = 0
        logger.info("Total object count reset")

# References:

# [1] OpenCV: Canny Edge Detection. (n.d.). Retrieved January 2, 2023, from https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
