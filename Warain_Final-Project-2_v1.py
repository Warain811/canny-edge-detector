# Program Description: Application that opens, reads, and transforms image files
# Author: John Cedric R. Warain, 4 - BSCS

from re import L
from tkinter import Y
import cv2      # import modules
import io  
import os
from os.path import exists
import PySimpleGUI as sg
import struct 
import matplotlib.pyplot as plt   
from PIL import Image, ImageTk  #Image for open, ImageTk for display
import numpy as np
import math
import random
import sys
import imutils

from open_image import ImageViewer

sg.theme('DarkGrey8')   # theme of the program
font = ("04b03", 12)     # font style of the program

file_column = [     # left column of the program
    [
        sg.Text("File Name:", text_color = "yellow"),       # text element
        sg.Input(size=(26, 1), disabled = True, text_color = "black", key="-FILE-"),    # input element with key 'FILE'
        sg.Button('Browse'),        # 'browse' button element
        sg.Button("Load Image"),    # 'load image' button element 
    ],

    [
        sg.Text("Load History:", size = (60, 1), text_color = "yellow", justification='center')   # text element  
    ],

    [
        sg.Listbox      # listbox element that shows the list of images that were previously loaded
        (
            values=[], 
            enable_events=True, 
            size=(55, 7), 
            key="-FILE LIST-", 
            horizontal_scroll=True
        ),
    ],

    [sg.Text("Edge Detection Options:", size = (60, 1), text_color = "yellow", justification='center'), ], # text element

    [
        sg.Button('Canny Algorithm', image_filename ='canny_edge_detector.png', pad = ((5, 0), (0, 0)), border_width = 1, tooltip=" Canny Edge Detector "),     # button elements that deal with transforming the image
        sg.Button('R', image_filename ='canny_edge_detector.png', pad = ((5, 0), (0, 0)), border_width = 1),     # button elements that deal with transforming the image
    
    ],
]

image_viewer_column = [     # right column of the program

[sg.Text("View of the image:", text_color = "yellow", justification = 'center')],     # text elements

[
    sg.Image(key="-IMAGE-", size = (320, 240), filename="empty.png"),   # image elements
    sg.Image(key="-colorpalette-", size = (90, 90)),                  
], 

]

transformation_column = [

    [sg.Text(size=(45, 1), key="-transformation-", text_color = "yellow", justification = 'center')],   # elements from 217-229  
    [sg.Image(key="-transformed_image-", size = (320, 240))],                                              # are for image transforming
]

layout = [      # this defines the window's contents
    [
        sg.Column(file_column, vertical_alignment='center', p = ((0, 3), (60, 75))),    # column element
        sg.VSeperator(),       # this is a vertical line that shows the separation of the columns
        sg.Column(image_viewer_column, element_justification = "center", expand_y= True),   # column element
        sg.VSeperator(),       # this is a vertical line that shows the separation of the columns
        sg.Column(transformation_column, element_justification = "center", expand_y= True),   # column element
    ]
]

window = sg.Window("Image Viewer", layout, font = font, resizable = True, finalize = True, size = (1500, 650))   # this showcases the layout of our program in a window

def main(file_list): 

    current_image = ""
    imageViewerFunctions = ImageViewer(window) 

    while True:     # event loop

        event, values = window.read()   # this is for displaying and interacting with the window

        if event == "Exit" or event == sg.WIN_CLOSED:   # this is to exit the program
            break

        elif event == "Browse":       # this lets the user choose the image from a directory
            file_path = sg.popup_get_file(file_types =  # file types that are allowed for the application, this gets the file path of the image
            [
                ("PCX (*.pcx)", "*.pcx"),
                ("JPEG (*.jpg)", "*.jpg"),
                ("PNG (*.png)", "*.png"),
                ("GIF (*.gif)", "*.gif"), 
                ("All files (*.*)", "*.*")
            ], 
            no_window= True, message = "")

            window['-FILE-'].update(os.path.basename(file_path))    # this updates the input element-
                                                                    # (with the key '-FILE-') with the file name of the image

        elif event == "-FILE LIST-":    # call image_open() whenever the the user clicks on the list box element
            try:
                imageViewerFunctions.clear_info()    

                fileListPath = values["-FILE LIST-"][0]     
                imageViewerFunctions.image_open(fileListPath)

                current_image = fileListPath
                imageViewerFunctions.clear_color_pallete(current_image)

            except:
                pass

        elif event == "Load Image":         # this  updates the file history whenever an image has been loaded,-
            imageViewerFunctions.clear_info()

            file_exist = values['-FILE-']      # and views the image
            
            if file_exist == "":
                pass

            elif not file_exist.endswith(('.gif', '.jpg', '.png', '.pcx', '.bmp')): # show error when user didn't choose an image
                sg.Popup("Please choose an image file.", font = font, button_type = 5, title = "Error!")

            else:
                file_list.append(file_path)                # if user has chosen a image, append its file path to the list inside the listbox,-
                window["-FILE LIST-"].update(file_list)    # and call image_open()

                if os.path.exists(file_path):
                    imageViewerFunctions.image_open(file_path)

                current_image = file_path
                imageViewerFunctions.clear_color_pallete(current_image)

        elif event == "R":       # apply negative transformation 
            if current_image == "":
                pass

            else:
                imageViewerFunctions.clear_info()
                imageViewerFunctions.clear_color_pallete(current_image)
                imageViewerFunctions.convert_to_PNG(current_image)

                image = cv2.imread("tmp.png")   #   cv2.imread() returns a BGR (Blue-Green-Red) array
                negative = image.copy()
                negative = abs(255 - negative[:,:,:])   # subtract 255 by the value of each pixel in each color channels
                cv2.imwrite("transformation.png", negative)

                imageViewerFunctions.transformation("-transformation-", "-transformed_image-", "Negative Transformation:")  # display negatively transformed image

        elif event == "Canny Algorithm":        

            if current_image == "":
                pass

            else:
                imageViewerFunctions.clear_info()
                imageViewerFunctions.clear_color_pallete(current_image)
                imageViewerFunctions.convert_to_PNG(current_image)
                

                image= cv2.imread("tmp.png")

                blurred = cv2.GaussianBlur(image, (5, 5), 0) # apply guassian blur to the image through a 5x5 kernel

                grayscale_image= cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY) # convert to a grayscale image
                detectedEdges = cv2.Canny(grayscale_image, 30, 150) # use canny edge detection algorithm to find the outlines of objects in images
                cv2.imshow("Edged", detectedEdges)

                # threshold the image by setting all pixel values less than 225
                # to 255 (white; foreground) and all pixel values >= 225 to 255
                # (black; background), thereby segmenting the image
                thresh = cv2.threshold(grayscale_image, 225, 255, cv2.THRESH_BINARY_INV)[1]
                cv2.imshow("Thresh", thresh)

                # a typical operation we may want to apply is to take our mask and
                # apply a bitwise AND to our input image, keeping only the masked 
                # regions
                mask = thresh.copy()
                output = cv2.bitwise_and(image, image, mask=mask)
                cv2.imshow("Output", output)

                # similarly, dilations can increase the size of the ground objects
                mask = thresh.copy()
                mask = cv2.dilate(mask, None, iterations=5)
                cv2.imshow("Dilated", mask)

                # find contours (i.e., outlines) of the foreground objects in the
                # thresholded image
                cv2.imshow("NIGGERS", thresh)
                cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                output = image.copy()
              
                print("Number of objects within image: ", len(cnts))
                
                # imageViewerFunctions.transformation("-transformation-", "-transformed_image-", "Detected Objects through Canny")  # display negatively transformed image

                # cv2.waitKey(0)

  

    imageViewerFunctions.delete_file("tmp.png")
    imageViewerFunctions.delete_file("transformation.png")
    imageViewerFunctions.delete_file("color_palette.png")
    
    window.close()    # this closes the window

if __name__ == "__main__":  # declare an empty file_list for the listbox element, 
                            # before we call the main function
    file_list = []
    main(file_list)