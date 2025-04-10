# open_image.py 
# This file contains the code related to displaying and opening the image

import io
import os
from os.path import exists
import struct 
from PIL import Image, ImageTk  
import numpy as np

from name_convention import UIVariables

ui_variables = UIVariables()

class ImageViewer():    
    def __init__(self, window):
        self.window = window
        self.current_image = ""
        self.file_list = []
        self.temporary_files = ['tmp.png', 'transformation.png']

    def convert_to_PNG(self, current_image):
        file_name = os.path.basename(current_image)
        
        if file_name.lower().endswith('.png'):
            self._convert_png(current_image)
        elif not file_name.lower().endswith('.pcx'):
            self._convert_standard_image(current_image)
        else:
            self._convert_pcx(current_image)

    def _convert_png(self, current_image):
        png = Image.open(current_image).convert('RGBA')
        png.load()
        background = Image.new("RGB", png.size, (255, 255, 255))
        background.paste(png, mask=png.split()[3])
        background.save('tmp.png', 'PNG')

    def _convert_standard_image(self, current_image):
        image = Image.open(current_image)
        RGB_image = image.convert("RGB")
        RGB_image.save("tmp.png")

    def _convert_pcx(self, current_image):
        with open(current_image, 'rb') as f:
            byte_data = []
            while (byte := f.read(1)):
                byte_data.append(int(struct.unpack('B', byte)[0]))

            color_palette = self._extract_color_palette(byte_data)
            image_data = self._process_pcx_data(byte_data, color_palette)
            image_data.save("tmp.png")

    def _extract_color_palette(self, byte_data):
        color_palette = []
        if len(byte_data) > 768:
            for i in range(len(byte_data) - 768, len(byte_data), 3):
                color_palette.append([
                    byte_data[i],
                    byte_data[i + 1],
                    byte_data[i + 2]
                ])
        return color_palette

    def _process_pcx_data(self, byte_data, color_palette):
        palette_image = self._create_color_palette_image(color_palette)
        image_data = Image.new('RGB', (256, 256), "black")
        pixels = image_data.load()
        
        image_color_values, palette_index = self._decode_pcx_data(byte_data)
        
        for i in range(0, 256 * 256):
            image_color_values[i] = color_palette[palette_index[i]]
            y = int(i / 256)
            x = int(i - (256 * y))
            pixels[x, y] = tuple(image_color_values[i])
            
        return image_data

    def _create_color_palette_image(self, color_palette):
        palette_image = Image.new('RGB', (64, 64), "black")
        pixels = palette_image.load()
        
        k = 0
        for i in range(0, palette_image.size[0], 4):
            for j in range(0, palette_image.size[1], 4):
                for x in range(4):
                    for y in range(4):
                        pixels[i + x, j + y] = tuple(color_palette[k])
                k += 1
        
        return palette_image

    def _decode_pcx_data(self, byte_data):
        image_color_values = [[0 for x in range(3)] for y in range(256 * 256)]
        palette_index = []
        position = 128
        
        while position < len(byte_data) - 768:
            byte = byte_data[position]
            position += 1
            
            if (byte & 0xC0) == 0xC0 and position < (len(byte_data) - 768):
                run_length = byte & 0x3F
                run_value = int(byte_data[position])
                position += 1
            else:
                run_length = 1
                run_value = byte
                
            palette_index.extend([run_value] * run_length)
            
        return image_color_values, palette_index

    def clear_info(self):
        for key in [
            ui_variables.first_transformation,
            ui_variables.second_transformation,
            ui_variables.blur_image,
            ui_variables.edges_image,
            ui_variables.dilated_edges_image,
            ui_variables.contours_image,
            "-num_of_objects-"
        ]:
            self.window[key].update('')

    def reset(self):
        self.clear_info()
        self.window["-FILE LIST-"].update('')

    def transformation(self, transform_name, transform_image, transformation):
        image = Image.open("transformation.png")
        image.thumbnail((256, 256))
        self.window[transform_name].update(transformation)
        self.window[transform_image].update(data=ImageTk.PhotoImage(image))

    def delete_file(self, file_name):
        if exists(file_name):
            os.remove(file_name)

    def image_open(self, file):
        image = Image.open(file)
        image.thumbnail((256, 256))
        bio = io.BytesIO()
        image.save(bio, "PNG")
        self.window["-IMAGE-"].update(data=bio.getvalue())

