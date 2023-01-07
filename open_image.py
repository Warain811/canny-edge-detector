# open_image.py 
# This file contains the code related to displaying and opening the image

import io   # import module
import os
from os.path import exists
import struct 
from PIL import Image, ImageTk  
import numpy as np

from name_convention import namingConvention

variableForUI = namingConvention()     
variableForUI.variables()

class ImageViewer():    

    def __init__(self, window):
        self.window = window
        self.current_image = ""
        self.file_list = []

    def convert_to_PNG(self, current_image):    # this function converts the image to png file
        file_name = os.path.basename(current_image)  # get the image's filename only
        
        if(file_name.split(".")[1] == "png"):    # check if image is in PNG format 
            png = Image.open(current_image).convert('RGBA')  # convert the image into RGBA
            png.load()               # required for png.split()
            background = Image.new("RGB", png.size, (255, 255, 255)) # if the image has a transparent background, turn the background white
            background.paste(png, mask=png.split()[3])      # 3 is the alpha channel
            background.save('tmp.png', 'PNG')       # save the converted into a png file 

        elif(file_name.split(".")[1] != "pcx"):     # every other image format besides .png and .pcx
            image = Image.open(current_image)       # open the image
            RGB_image = image.convert("RGB")        # convert the image into RGB
            RGB_image.save("tmp.png")           # save the converted into a png file
        
        else:    # get pcx image data 
            with open(current_image, 'rb') as f:     # read the image as binary
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

                imageData = Image.new('RGB', (256, 256), "black")   # create a completely black 256x256 image for printing the actual image
                pixels = imageData.load()   # load the pixel map
                
                imageColorValues = [[0 for x in range(3)] for y in range(256 * 256)]    # the resulting image will have a height, width, and channel depth of 256, 256, and 3, respectively
                paletteIndex = []
                position = 128
                runlength = 0
                runvalue = 0

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
 
                imageData.save("tmp.png")
            f.close()
    
    # function to clear info
    def clear_info(self):           # clear and hide widgets whenever another image has been viewed
        self.window[variableForUI.first_transformation].update('')  
        self.window[variableForUI.second_transformation].update('')  
        self.window[variableForUI.blur_image].update('')  
        self.window[variableForUI.edges_image].update('')  
        self.window[variableForUI.dilated_edges_image].update('')  
        self.window[variableForUI.contours_image].update('')  
        self.window["-num_of_objects-"].update('')  

    # function to clear all info when user opens a new folder
    def reset(self):           
        self.clear_info()  
        self.window["-FILE LIST-"].update('') 

    # function to display the transformations being done to the image
    def transformation(self, transform_name, transform_image, transformation):
        image = Image.open("transformation.png")     # open the transformed image 
        image.thumbnail((256, 256))     # resize the image
        self.window[transform_name].update(transformation)   
        self.window[transform_image].update(data = ImageTk.PhotoImage(image))    # display the image's respective transformation  
    
    # function to delete the image files 
    def delete_file(self, file_name):     
        file_exists = exists(file_name)
        if file_exists:  
            os.remove(file_name)
    
    # function to view an image 
    def image_open(self, file):   
        image = Image.open(file)    # open the file
        image.thumbnail((256, 256))     # resize the image
        bio = io.BytesIO()  # convert image into a byte stream
        image.save(bio, "PNG")      # save the image as PNG
        self.window["-IMAGE-"].update(data = bio.getvalue())     # show the image
    
