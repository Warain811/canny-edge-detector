# Program Description: This program detects the objects within images through the Canny Edge Detection Algorithm

# main.py
# This file contains the code for the UI of the program

import cv2      # import modules and classes
import os
from os.path import exists
import PySimpleGUI as sg   
import numpy as np

from open_image import ImageViewer  
from canny_edge_detector import edgeDetection
from name_convention import namingConvention

sg.theme('DarkGrey8')   # theme of the program
font = ("Arial", 12)     # font style of the program

variableForUI = namingConvention()
variableForUI.variables()

file_column = [     # left column of the program
    [
        sg.Text("Folder Path:", text_color = "yellow"),       
        sg.Input(size=(26, 1), disabled = True, text_color = "black", key="-FOLDER-"),    # input element with key 'FOLDER'
        sg.Button('Browse'),        # 'browse' button element
        sg.Button("Load Images\n and Detect Objects", size = (18,2) ),    # 'load image' button element 
    ],

    [
        sg.Text("Images Found From Folder:", size = (60, 1), text_color = "yellow", justification='center')   
    ],

    [
        sg.Listbox      # listbox element that shows the list of images inside the folder
        (
            values=[], 
            enable_events=True, 
            size=(55, 7), 
            key="-FILE LIST-", 
            horizontal_scroll=True
        ),
    ],

    [sg.Text("Total Number of Objects Detected from Images in Folder: ", size = (60, 1), key='-OBJECTS-', text_color = "yellow", justification='center'), ], 
    
    [sg.Text("Hysteresis Threshold Values: ", size=(40, 1), text_color = "white", justification = 'center', p=((0, 0), (30, 0)) ),],

    [sg.Text("Min Value: ", size=(60, 1), text_color = "yellow", justification = 'center', p=((0, 0), (0, 5)) ) ],
    [sg.Slider(range = (0, 255), default_value = 0, orientation='h', size=(30, 20),  key="-cannyMinValue-") ],

    [sg.Text("Max Value: ", size=(60, 1), text_color = "yellow", justification = 'center', p=((0, 0), (0, 5)) )],
    [sg.Slider(range = (0, 255), default_value = 70, orientation='h', size=(30, 20), key="-cannyMaxValue-")]

]

image_viewer_column = [     # center column of the program

[sg.Text("View of the image:", text_color = "yellow", justification = 'center')],     

[
    sg.Image(key="-IMAGE-", size = (320, 240), filename="empty.png"),   # image element                 
], 

]

transformation_column = [   # right column of the program
    [sg.Text(size=(60, 2), key = variableForUI.first_transformation, text_color = "yellow", justification = 'center')],    
    [   
        sg.Image(key = variableForUI.blur_image, size = (320, 240), pad = ((0, 10), (0, 25)) ),
        sg.Image(key = variableForUI.edges_image, size = (320, 240), pad = ((0, 0), (0, 25)) ),
    ],  
    [sg.Text(size=(60, 2), key = variableForUI.second_transformation, text_color = "yellow", justification = 'center')],    
    [
        sg.Image(key = variableForUI.dilated_edges_image, size = (320, 240) ),
        sg.Image(key = variableForUI.contours_image, size = (320, 240) ),
    ],  
    [sg.Text(size=(60, 1), key="-num_of_objects-", text_color = "yellow", justification = 'center')],                                               
]

layout = [      # the layout defines the window's contents
    [
        sg.Column(file_column, vertical_alignment='center', element_justification = 'center', p = ((0, 3), (60, 75))),    # column element
        sg.VSeperator(),       # this is a vertical line that shows the separation of the columns
        sg.Column(image_viewer_column, element_justification = "center", expand_y= True),   # column element
        sg.VSeperator(),       # this is a vertical line that shows the separation of the columns
        sg.Column(transformation_column, element_justification = "center", expand_y= True),   # column element
    ]
]

window = sg.Window("Object Detection through Canny Algorithm", layout, font = font, resizable = True, finalize = True, size = (1500, 710))   # this showcases the layout of the program in a window

def main():    

    imageViewerFunctions = ImageViewer(window) 
    cannyEdgeDetection = edgeDetection() 

    while True:     # event loop that will run the selected event based on the action of the user of the program

        event, values = window.read()   # this is for displaying and interacting with the window

        if event == "Exit" or event == sg.WIN_CLOSED:   # this is to exit the program
            break

        elif event == "Browse":       # this lets the user select a folder
            file_path = sg.popup_get_folder(no_window= True, message = "")

            if file_path == "":     
                sg.Popup("Please choose a folder. Program will use previously loaded folder.", font = font, button_type = 5, title = "Error!")
            else:
                window['-FOLDER-'].update(file_path)  

        elif event == "Load Images\n and Detect Objects":    # load the images from the folder, and run the canny algorithm to detect the objects
            
            folder = values['-FOLDER-']     

            if folder == "":
                sg.Popup("Please choose a nonempty folder. Program will use previously loaded folder.", font = font, button_type = 5, title = "Error!")

            else:
                
                cannyMinValue = (int(values['-cannyMinValue-'])) 
                cannyMaxValue = (int(values['-cannyMaxValue-']))
                
                if(cannyMinValue > cannyMaxValue):   # if the min value is greater than the max value, then the algorithm won't run
                    sg.Popup("Min value cannot exceed max value.", font = font, button_type = 5, title = "Error!")

                else:  # if  the min value is lesser or equal to the max value, then the canny algorithm will run [1]
                    imageViewerFunctions.reset() 
                    cannyEdgeDetection.resetTotalNumberOfObjects()

                    try:
                        fileList = os.listdir(folder)
                    except:
                        fileList = []
                    
                    fileNames = [
                        f
                        for f in fileList
                        if os.path.isfile(os.path.join(folder, f))
                        and f.lower().endswith(('.gif', '.jpg', '.png', '.pcx', '.bmp'))
                    ]

                    if fileNames == []:
                        sg.Popup("Chosen folder is empty. Please choose a different folder", font = font, button_type = 5, title = "Warning!")

                    window["-FILE LIST-"].update(fileNames)

                    filePathsInList = []

                    for i in range(len(fileNames)):
                        filePathsInList.append(os.path.join(
                        values["-FOLDER-"], fileNames[i]
                        ) )
            
                    for j in range(len(filePathsInList)):
                        imageViewerFunctions.convert_to_PNG(filePathsInList[j]) 
                        cannyEdgeDetection.detectEdges('tmp.png', cannyMinValue, cannyMaxValue)
                        cannyEdgeDetection.getTotalNumberOfObjects() # get the total number of objects from the images inside the folder
                        
                    window["-OBJECTS-"].update("Total Number of Objects Detected from Images in Folder: "+ str(cannyEdgeDetection.totalNumberOfObjects)) # display total number of detected objects from all images inside the folder
                    
        elif event == "-FILE LIST-":    # view the image and the transformations it has went through whenever the the user clicks on an image from the list box 
            try:
                imageViewerFunctions.clear_info()   

                fileListPath = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                ) 
    
                imageViewerFunctions.convert_to_PNG(fileListPath)  # convert the image to pnf
                imageViewerFunctions.image_open('tmp.png')      # view the image
                cannyEdgeDetection.detectEdges('tmp.png', cannyMinValue, cannyMaxValue) # run the canny algorithm  

                cv2.imwrite("transformation.png", cannyEdgeDetection.blurredImage)      
                imageViewerFunctions.transformation(variableForUI.first_transformation, variableForUI.blur_image, "")  # display the blurred grayscale image
                
                cv2.imwrite("transformation.png", cannyEdgeDetection.edges)  
                imageViewerFunctions.transformation(variableForUI.first_transformation, variableForUI.edges_image, "Gaussian Blurred, Grayscaled Image, \n and Edges Detected through Canny Algorithm (left to right):")   # display the edges in the image

                cv2.imwrite("transformation.png", cannyEdgeDetection.dilatedEdges)  
                imageViewerFunctions.transformation(variableForUI.second_transformation, variableForUI.dilated_edges_image, "")  # display dilated edges of the image

                result = np.zeros_like(cannyEdgeDetection.image)
                cv2.drawContours(result, cannyEdgeDetection.contours, -1, (0,255,0), thickness=-1)  # fill the external contours of the image
                cv2.imwrite("transformation.png", result)

                imageViewerFunctions.transformation(variableForUI.second_transformation, variableForUI.contours_image, "Dilated Edges, \n and External Contours Filled (left to right):")  # display filled contours in image 
                window["-num_of_objects-"].update("Total number of objects detected in selected image: " + str(cannyEdgeDetection.numberOfObjects))    # display number of objects detected in the selected image            

            except:
                pass
                
    imageViewerFunctions.delete_file("tmp.png")
    imageViewerFunctions.delete_file("transformation.png")
    
    window.close()    # this closes the window

if __name__ == "__main__":  # call the main function
    main()

# References:

# [1] Driscoll, M. (n.d.). PySimpleGUI: The Simple Way to Create a GUI With Python – Real Python. Retrieved January 5, 2023, from https://realpython.com/pysimplegui-python/



