# Canny Edge Detector

A Python application that detects and counts objects in images using the Canny Edge Detection algorithm. Users can adjust minimum and maximum values for double threshold to fine-tune the edge detection.

## Author
John Cedric R. Warain

## Specifications
This project showcases the implementation of the Canny Edge Detection Algorithm through a user-friendly interface. The application:
- Allows users to load multiple images from a folder
- Provides real-time adjustment of threshold values
- Displays step-by-step image transformations
- Counts objects in individual images and total objects in a folder
- Supports multiple image formats (PNG, JPG, GIF, PCX, BMP)

## Features
- Interactive GUI built with PySimpleGUI
- Real-time edge detection parameter adjustment
- Visualization of processing steps:
  - Original image
  - Gaussian blurred grayscale
  - Edge detection
  - Dilated edges
  - Contour detection
- Batch processing of multiple images

## Requirements
- Python 3.x
- OpenCV (cv2)
- NumPy
- PIL (Python Imaging Library)
- PySimpleGUI

See `requirements.txt` for specific version requirements.

## Installation
1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the program:
```bash
python main.py
```
2. Click 'Browse' to select a folder containing images
3. Adjust the min/max threshold values using the sliders
4. Click 'Load Images and Detect Objects' to process the images with the adjusted threshold
5. Click on individual images in the list to view their processing steps

## Sample Images
Sample images are provided in the `images/` directory for testing.

For more information and documentation: https://docs.google.com/document/d/1q5ZXYupFWGPXcGGxJmdD5IFbjJjkT3tOtuv9vRDkgZA/edit?usp=sharing
