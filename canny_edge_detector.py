# canny_edge_detector.py 
# This file contains the code related to the Canny algorithm used to detect objects within the image 

import cv2   # import module

class edgeDetection():
    def __init__(self):
        self.image = []
        self.blurredImage = []
        self.edges = []
        self.dilatedEdges = []
        self.contours = []
        self.totalNumberOfObjects = 0
        self.numberOfObjects = 0

    def detectEdges(self, filepath, cannyMinValue, cannyMaxValue):
        """Detects edges in an image using the Canny edge detection algorithm.
        
        Args:
            filepath (str): Path to the image file
            cannyMinValue (int): Lower threshold for the hysteresis procedure
            cannyMaxValue (int): Upper threshold for the hysteresis procedure
        """
        self.image = cv2.imread(filepath)
        self._preprocess_image()
        self._detect_canny_edges(cannyMinValue, cannyMaxValue)
        self._find_contours()
    
    def _preprocess_image(self):
        """Convert image to grayscale and apply Gaussian blur."""
        imgray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.blurredImage = cv2.GaussianBlur(imgray, (5, 5), 0)
    
    def _detect_canny_edges(self, minVal, maxVal):
        """Apply Canny edge detection algorithm."""
        self.edges = cv2.Canny(
            self.blurredImage,
            minVal,
            maxVal,
            L2gradient=True,
            apertureSize=3
        )
        self.dilatedEdges = cv2.blur(self.edges, (3, 3), 0)
    
    def _find_contours(self):
        """Find external contours in the image."""
        contours, _ = cv2.findContours(
            self.dilatedEdges.copy(),
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )
        self.contours = contours
        self.numberOfObjects = len(contours)
    
    def getTotalNumberOfObjects(self):
        """Update the total count of objects across all processed images."""
        self.totalNumberOfObjects += self.numberOfObjects
    
    def resetTotalNumberOfObjects(self):
        """Reset the total object count when loading a new folder."""
        self.totalNumberOfObjects = 0

# References:

# [1] OpenCV: Canny Edge Detection. (n.d.). Retrieved January 2, 2023, from https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
