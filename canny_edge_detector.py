import cv2

class edgeDetection():

    def __init__(self, ):
        self.edges = []
        self.dilatedEdges = []
        self.contours = []
        self.image = []
        self.totalNumberOfObjects = 0
        self.numberOfObjects = 0

    def detectEdges(self, filepath,canny_scalex,canny_scaley):
        im = cv2.imread(filepath)
        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

        imgray = cv2.GaussianBlur(imgray, (5, 5), 0)
        detectedEdges = cv2.Canny(imgray, canny_scalex,canny_scaley, L2gradient= True, apertureSize=3) # use canny edge detection algorithm to find the outlines of objects in images
        dilatedEdges = cv2.blur(detectedEdges, (3, 3), 0)

        contours, hierarchy = cv2.findContours(dilatedEdges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        self.image = im
        self.blurredImage = imgray
        self.edges = detectedEdges
        self.dilatedEdges = dilatedEdges
        self.contours = contours
        self.numberOfObjects = len(contours)
    
    def getTotalNumberOfObjects(self):
        self.totalNumberOfObjects = self.totalNumberOfObjects + self.numberOfObjects
    
    def resetTotalNumberOfObjects(self):
        self.totalNumberOfObjects = 0

 