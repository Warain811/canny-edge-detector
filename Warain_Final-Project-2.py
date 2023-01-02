# Program Description: Desktop Application that opens, reads, and transforms image files
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

def main(file_list): 

    flag = 0
    current_image = ""

    # function to convert any image file into a png
    def convert_to_RGB(current_image):
        file_name = os.path.basename(current_image)  # get the image's filename only
        
        if(file_name.split(".")[1] == "png"):    # check if image is in PNG format [1] [2]
            png = Image.open(current_image).convert('RGBA')  # convert the image into RGBA
            png.load()               # required for png.split()
            background = Image.new("RGB", png.size, (255, 255, 255)) # if the image has a transparent background, turn the background white
            background.paste(png, mask=png.split()[3])      # 3 is the alpha channel
            background.save('tmp.png', 'PNG')       # save the converted into a png file 

        elif(file_name.split(".")[1] != "pcx"):     # every other image format besides .png and .pcx
            image = Image.open(current_image)       # open the image
            RGB_image = image.convert("RGB")        # convert the image into RGB
            RGB_image.save("tmp.png")           # save the converted into a png file

    # function to display the image
    def transformation(transform_name, transform_image, transformation):
        image = Image.open("transformation.png")     # open the transformed image [1]
        image.thumbnail((256, 256))     # resize the image
        window[transform_name].update(transformation)   
        window[transform_image].update(data = ImageTk.PhotoImage(image))    # display the image's respective transformation
    
    # function to show the update the slider
    def clear_info():           # clear and hide widgets whenever another image has been viewed
        window["-transformation-"].update('')  
        window["-transformed_image-"].update('')     
    
    # function to clear the colour palette image
    def clear_color_pallete(current_image):     # clear color palette if current image is not in pcx format
        file_name = os.path.basename(current_image)  
        if(file_name.split(".")[1] != "pcx"):
            window["-colorpalette-"].update('') 

    # function to open an image and the header information
    def image_open(file):   # function for opening an image

        file_name = os.path.basename(file)  # get the image's filename only
        if(file_name.split(".")[1] != "pcx"):    # check if image is not in PCX format
            image = Image.open(file)    # open the file
            image.thumbnail((256, 256))     # resize the image
            bio = io.BytesIO()  # convert image into a byte stream
            image.save(bio, "PNG")      # save the image as PNG
            window["-IMAGE-"].update(data = bio.getvalue())     # show the image
    
        else:   # get pcx image data [15]
            with open(file, 'rb') as f:     # read the image as binary
                byte_data = []
                while (byte := f.read(1)):      # read all the bytes in the image
                    byte_data.append(int(struct.unpack('B', byte)[0]))
    
                ColorPalette = []           #list representing the color palette
                if (len(byte_data) > 768):          #  color palette is found 768 bytes from the end of the file
                    for i in range(int(len(byte_data)) - 768, int(len(byte_data)), 3):     # the palette is stored as a sequence of RGB triples
                        temp_array = []
                        temp_array.append([byte_data[i], byte_data[i + 1], byte_data[i + 2]])       # group the RGB triples together to represent the color palette
                        ColorPalette.extend(temp_array)

                # PIL accesses images in Cartesian co-ordinates, so it is Image[columns, rows]
                color_palette = Image.new('RGB', (64, 64), "black") # create a completely black 64x64 image for the color palette
                pixels = color_palette.load()   # create the pixel map

                k = 0
                for i in range(0, color_palette.size[0], 4):    # for every column (color_palette.size[0] gets the width)
                    for j in range(0, color_palette.size[1], 4):    # for every row (color_palette.size[1] gets the height)
                        for x in range(4):              # 4x4 boxes will represent a colour
                            for y in range(4):
                                pixels[i + x, j + y] = (ColorPalette[k][0], ColorPalette[k][1], ColorPalette[k][2]) # set the colour accordingly for the pixel located in each column and row in the pixel map
                        k = k + 1  

                color_palette.save("color_palette.png")
                window["-colorpalette-"].update("color_palette.png")     # save and show the color palette

                imageData = Image.new('RGB', (256, 256), "black")   # create a completely black 256x256 image for printing the actual image
                pixels = imageData.load()   # load the pixel map
                
                imageColorValues = [[0 for x in range(3)] for y in range(256 * 256)]    # the resulting image will have a height, width, and channel depth of 256, 256, and 3, respectively
                paletteIndex = []
                position = 128
                runlength = 0
                runvalue = 0

                full_image = np.zeros([256, 256, 3])
                while (position < int(len(byte_data) - 768) ):  # this range represents where the image data is located ( 128 bytes < position < (byte_data - 768))
                    Byte = byte_data[position]   
                    position = position + 1

                    if ((Byte & 0xC0) == 0xC0 and position < (len(byte_data) - 768)):  # RLE pair representing a series of several pixels of a single value
                        runlength = (Byte & 0x3F)            # run length have a value range of 0-63, and its length can be extracted through bitwise addition 
                        runvalue = int(byte_data[position])          # run value represents the given palette index for the pixels
                        position = position + 1

                    else:   # any other case, the byte is interpreted as a single pixel value of a given palette index or color value
                        runlength = 1
                        runvalue = Byte 
                    
                    for j in range(0, runlength):
                        paletteIndex.append(runvalue)
                
                for i in range(0, 256 * 256):
                    imageColorValues[i] = ColorPalette[paletteIndex[i]] # get the color from the color palette
                    y = int(i / 256)                # get the x and y coordinate for the pixel  
                    x = int(i - (256 * y))
                    pixels[x, y] = (imageColorValues[i][0], imageColorValues[i][1], imageColorValues[i][2]) # set the  color of the pixel in the appropriate pixel map
                    full_image[y][x] = (imageColorValues[i][0], imageColorValues[i][1], imageColorValues[i][2])
                
                full_image = np.array(full_image)
                image_dimensions = np.array(full_image)
                full_image = full_image.reshape(full_image.shape[0] * full_image.shape[1], 3)

                new_array = [tuple(row) for row in full_image]
                colorpalette, counter = np.unique(new_array, axis=0, return_counts=True)

                color_palette = np.uint8(np.array([val for (_, val) in sorted(zip(counter, colorpalette), key=lambda x: x[0], reverse=True)])) # sort color palette- 
                                                                                                                                    # based on most frequently used
                imageData.save("tmp.png")
                window["-IMAGE-"].update("tmp.png")     # save and show the image

            f.close()
    
    # function to delete the image files 
    def delete_file(file_name):     # delete the generated images
        file_exists = exists(file_name)
        if file_exists:  
            os.remove(file_name)

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
                clear_info()     

                file_list_name = values["-FILE LIST-"][0]     
                image_open(file_list_name)

                current_image = file_list_name
                clear_color_pallete(current_image)
            except:
                pass

        elif event == "Load Image":         # this  updates the file history whenever an image has been loaded,-
            clear_info()

            file_exist = values['-FILE-']      # and views the image
            
            if file_exist == "":
                pass

            elif not file_exist.endswith(('.gif', '.jpg', '.png', '.pcx', '.bmp')): # show error when user didn't choose an image
                sg.Popup("Please choose an image file.", font = font, button_type = 5, title = "Error!")

            else:
                file_list.append(file_path)                # if user has chosen a image, append its file path to the list inside the listbox,-
                window["-FILE LIST-"].update(file_list)    # and call image_open()
                if os.path.exists(file_path):
                    image_open(file_path)

                current_image = file_path
                clear_color_pallete(current_image)

        elif event == "Canny":         # this  updates the file history whenever an image has been loaded,-
            pass

    delete_file("tmp.png")
    delete_file("transformation.png")
    delete_file("color_palette.png")
    
    window.close()    # this closes the window

if __name__ == "__main__":  # declare an empty file_list for the listbox element, 
                            # before we call the main function
    file_list = []
    main(file_list)