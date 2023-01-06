# canny_edge_detector.py 
# This file contains the code related to the Canny algorithm used to detect objects within the image 

import cv2   # import module

class edgeDetection():

    def __init__(self, ):
        self.image = []
        self.blurredImage = []
        self.edges = []
        self.dilatedEdges = []
        self.contours = []
        self.totalNumberOfObjects = 0
        self.numberOfObjects = 0

    def detectEdges(self, filepath, cannyMinValue, cannyMaxValue):  # this function detects the edges from the image [1]
        im = cv2.imread(filepath)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)   # turn the image into grayscale

        imgray = cv2.GaussianBlur(imgray, (5, 5), 0)    # gaussian blur the image
        detectedEdges = cv2.Canny(imgray, cannyMinValue, cannyMaxValue, L2gradient= True, apertureSize=3) # use canny edge detection algorithm to detect the edges of the objects in the images 
        dilatedEdges = cv2.blur(detectedEdges, (3, 3), 0)       # dilate the edges

        contours, hierarchy = cv2.findContours(dilatedEdges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)     # find the external contours of the image
        
        self.image = im
        self.blurredImage = imgray
        self.edges = detectedEdges
        self.dilatedEdges = dilatedEdges
        self.contours = contours
        self.numberOfObjects = len(contours)
    
    def getTotalNumberOfObjects(self):    # this function gets the total number of objects from the images inside the folder
        self.totalNumberOfObjects = self.totalNumberOfObjects + self.numberOfObjects
    
    def resetTotalNumberOfObjects(self):    # this function resets the total number of objects when the user loads a new folder 
        self.totalNumberOfObjects = 0

# References:

# [1] OpenCV: Canny Edge Detection. (n.d.). Retrieved January 2, 2023, from https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
