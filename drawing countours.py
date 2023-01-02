import numpy as np
import cv2
import imutils

im = cv2.imread('bugs.jpg')
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

imgray = cv2.GaussianBlur(imgray, (5, 5), 0)
detectedEdges = cv2.Canny(imgray, 0, 70, L2gradient= True, apertureSize=3) # use canny edge detection algorithm to find the outlines of objects in images
detectedEdges = cv2.blur(detectedEdges, (3, 3), 0)

# ret, thresh = cv2.threshold(imgray, 127, 255, 0)
cv2.imshow('threshold', detectedEdges)
# print(thresh)
contours, hierarchy = cv2.findContours(detectedEdges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = imutils.grab_contours(contours)

print(len(contours))
result = np.zeros_like(im)
cv2.drawContours(result, contours, -1, (0,255,0), thickness=-1)
cv2.imshow('result', result)

cv2.waitKey(0)
cv2.destroyAllWindows()