# Description:              Python script provides a set of image processing functions using the Pillow library. This file contains helper functions for image processing using the Pillow library.
# Purpose:                  Perform specific image transformations but do not handle web requests.
# File Name:                image_processing.py
# File Type:                Utility Module
# Installations:            Pillow, Requests
# Functions (Re-Usable):    compress_image(), rotate_image(), apply_filter(), create_thumbnail(), mask_image(), load_image_from_url(). These reusable image processing functions can be used in other projects or scts without modifying main.py.
# Note:                     It can be independently tested image_processing.py without running the FastAPI server. Unit testing image functions becomes easier with frameworks like pytest.
# Author:                   Nagarjun Gutha Chandrasekaran
# Date:                     02/26/2025
# Version:                  1.0
# Modifications:

from PIL import Image, ImageFilter, ImageOps
import io
import requests

def resize_image(img, width, height):
    return img.resize((width, height))

def apply_filter(img, filter_type):
    if filter_type == "grayscale":
        return img.convert("L")
    elif filter_type == "sepia":
        sepia_img = img.convert("RGB")
        sepia_data = [(int(r * 0.393 + g * 0.769 + b * 0.189),
                       int(r * 0.349 + g * 0.686 + b * 0.168),
                       int(r * 0.272 + g * 0.534 + b * 0.131))
                      for (r, g, b) in sepia_img.getdata()]
        sepia_img.putdata(sepia_data)
        return sepia_img
    elif filter_type == "blur":
        return img.filter(ImageFilter.BLUR)
    else:
        return img

def compress_image(img, quality=50):
    output_io = io.BytesIO()
    img.save(output_io, format="JPEG", quality=quality)
    output_io.seek(0)
    return Image.open(output_io)

def rotate_image(img, degrees):
    return img.rotate(degrees)

def create_thumbnail(img):
    img.thumbnail((100, 100))
    return img

def mask_image(img):
    """Applies an elliptical mask to the image."""
    mask = Image.new("L", img.size, 0)
    mask = ImageOps.fit(mask, img.size, centering=(0.5, 0.5))
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    img.putalpha(mask)
    return img

def load_image_from_url(url):
    """Loads an image from a given URL."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content))
    return img
