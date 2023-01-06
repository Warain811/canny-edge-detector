# Program Description: Application that opens, reads, and transforms image files
# Author: John Cedric R. Warain, 4 - BSCS

from re import L
from tkinter import Y
import cv2      # import modules
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
        sg.Text("Folder Path:", text_color = "yellow"),       # text element
        sg.Input(size=(26, 1), disabled = True, text_color = "black", key="-FOLDER-"),    # input element with key 'FILE'
        sg.Button('Browse'),        # 'browse' button element
        sg.Button("Load Images\n and Detect Objects", size = (18,2) ),    # 'load image' button element 
    ],

    [
        sg.Text("Images Found From Folder:", size = (60, 1), text_color = "yellow", justification='center')   # text element  
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

    [sg.Text("Total Number of Objects Detected from Images in Folder: ", size = (60, 1), key='-OBJECTS-', text_color = "yellow", justification='center'), ], 
   
    [sg.Text("Canny Threshold: ", size=(40, 1), text_color = "yellow", justification = 'center', p=(0,35)),],

    [
     sg.Text("Min Value: ", size=(60, 1), text_color = "yellow",justification = 'center', p=(0,2)),],[
     sg.Slider(range=(0, 255),default_value=0, orientation='h', size=(30, 20),  key="-canny_scalex-",),
    ],
    [
     sg.Text("Max Value: ", size=(60, 1), text_color = "yellow",justification = 'center', p=(0,2)),],[
     sg.Slider(range=(0, 255),default_value=70, orientation='h', size=(30, 20), key="-canny_scaley-"),
    ],                                        
]

image_viewer_column = [     # right column of the program

[sg.Text("View of the image:", text_color = "yellow", justification = 'center')],     # text elements

[
    sg.Image(key="-IMAGE-", size = (320, 240), filename="empty.png"),   # image elements                 
], 

]

transformation_column = [
    [sg.Text(size=(60, 2), key = variableForUI.first_transformation, text_color = "yellow", justification = 'center')],    
    [   
        sg.Image(key = variableForUI.blur_image, size = (320, 240), pad = ((0, 10), (0, 25)) ),
        sg.Image(key = variableForUI.edges_image, size = (320, 240), pad = ((0, 0), (0, 25))),
    ],  
    [sg.Text(size=(60, 2), key = variableForUI.second_transformation, text_color = "yellow", justification = 'center')],    
    [
        sg.Image(key = variableForUI.dilated_edges_image, size = (320, 240)),
        sg.Image(key = variableForUI.contours_image, size = (320, 240)),
    ],  
    [sg.Text(size=(60, 1), key="-num_of_objects-", text_color = "yellow", justification = 'center')],                                               
]

layout = [      # this defines the window's contents
    [
        sg.Column(file_column, vertical_alignment='center',element_justification = "center", p = ((0, 3), (60, 75))),    # column element
        sg.VSeperator(),       # this is a vertical line that shows the separation of the columns
        sg.Column(image_viewer_column, element_justification = "center", expand_y= True),   # column element
        sg.VSeperator(),       # this is a vertical line that shows the separation of the columns
        sg.Column(transformation_column, element_justification = "center", expand_y= True),   # column element
    ]
]

window = sg.Window("Object Detection through Canny Algorithm", layout, font = font, resizable = True, finalize = True, size = (1500, 710))   # this showcases the layout of our program in a window

def main(): 

    imageViewerFunctions = ImageViewer(window) 
    cannyEdgeDetection = edgeDetection() 

    while True:     # event loop

        event, values = window.read()   # this is for displaying and interacting with the window

        if event == "Exit" or event == sg.WIN_CLOSED:   # this is to exit the program
            break

        elif event == "Browse":       # this lets the user choose the image from a directory
            file_path = sg.popup_get_folder(no_window= True, message = "")

            if file_path == "":
                sg.Popup("Please choose a folder. Program will use previously loaded folder.", font = font, button_type = 5, title = "Error!")
            else:
                window['-FOLDER-'].update(file_path)  # this updates the input element-

        elif event == "Load Images\n and Detect Objects":         # this  updates the file history whenever an image has been loaded,-
            canny_scalex = (int(values['-canny_scalex-']))
            canny_scaley = (int(values['-canny_scaley-']))
     
            folder = values['-FOLDER-']      # and views the image

            if folder == "":
                sg.Popup("Please choose a nonempty folder. Program will use previously loaded folder.", font = font, button_type = 5, title = "Error!")

            else:
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
                    sg.Popup("Chosen folder is empty.", font = font, button_type = 5, title = "Warning!")

                window["-FILE LIST-"].update(fileNames)

                filePathsInList = []

                for i in range(len(fileNames)):
                    filePathsInList.append(os.path.join(
                    values["-FOLDER-"], fileNames[i]
                    ) )
        
                for j in range(len(filePathsInList)):
                    imageViewerFunctions.convert_to_PNG(filePathsInList[j]) 
                    cannyEdgeDetection.detectEdges('tmp.png',canny_scalex,canny_scaley)
                    cannyEdgeDetection.getTotalNumberOfObjects()
                    
                window["-OBJECTS-"].update("Total Number of Objects Detected from Images in Folder: "+ str(cannyEdgeDetection.totalNumberOfObjects))
                
        elif event == "-FILE LIST-":    # call image_open() whenever the the user clicks on the list box element
            canny_scalex = (int(values['-canny_scalex-']))
            canny_scaley = (int(values['-canny_scaley-']))
            
            try:
                imageViewerFunctions.clear_info()   

                fileListPath = os.path.join(
                    values["-FOLDER-"], values["-FILE LIST-"][0]
                ) 
    
                imageViewerFunctions.convert_to_PNG(fileListPath) 
                imageViewerFunctions.image_open('tmp.png') 
                cannyEdgeDetection.detectEdges('tmp.png',canny_scalex,canny_scaley)  

                cv2.imwrite("transformation.png", cannyEdgeDetection.blurredImage)
                imageViewerFunctions.transformation(variableForUI.first_transformation, variableForUI.blur_image, "")  # display detected objects in image 
                
                cv2.imwrite("transformation.png", cannyEdgeDetection.edges)
                imageViewerFunctions.transformation(variableForUI.first_transformation, variableForUI.edges_image, "Gaussian Blurred, Grayscaled Image, \n and Edges Detected through Canny Algorithm (left to right):")  # display detected objects in image 

                cv2.imwrite("transformation.png", cannyEdgeDetection.dilatedEdges)
                imageViewerFunctions.transformation(variableForUI.second_transformation, variableForUI.dilated_edges_image, "")  # display detected objects in image 

                result = np.zeros_like(cannyEdgeDetection.image)
                cv2.drawContours(result, cannyEdgeDetection.contours, -1, (0,255,0), thickness=-1)
                cv2.imwrite("transformation.png", result)

                imageViewerFunctions.transformation(variableForUI.second_transformation, variableForUI.contours_image, "Dilated Edges, \n and External Contours Filled (left to right):")  # display detected objects in image 
                window["-num_of_objects-"].update("Total number of objects detected in selected image: " + str(cannyEdgeDetection.numberOfObjects))                

            except:
                pass
                
    imageViewerFunctions.delete_file("tmp.png")
    imageViewerFunctions.delete_file("transformation.png")
    
    window.close()    # this closes the window

if __name__ == "__main__":  # call the main function
    main()
