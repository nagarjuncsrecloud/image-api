# Description:              Python script that defines a FastAPI-based web service / application that provides two API endpoints: /upload/ and /process/.
# Purpose:                  Handles API requests, file uploads, and routing. Acts as an API for uploading and processing images. It calls / imports the functions from image_processing.py when an API request is received and integrates them into API routes.
# File Name:                main.py
# File Type:                FastAPI Backend
# Installations:            FastAPI, Uvicorn, Pillow, Requests
# Functions (Re-Usable):    upload_image(), process_image()
# Note:                     main.py loads the image, applies the requested modification(s) / transformation(s) by using functions imported from image_processing.py, and saves the processed version.
# Author:                   Nagarjun Gutha Chandrasekaran
# Date:                     02/26/2025
# Version:                  1.0
# Modifications:

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from PIL import Image
import io
import os
import json
import requests
from image_processing import (
    resize_image, apply_filter, compress_image, rotate_image, 
    create_thumbnail, mask_image, load_image_from_url
)

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

# Ensure directory exists before saving
save_path = "downloaded_images/downloaded_image_from_url.jpg"
os.makedirs(os.path.dirname(save_path), exist_ok=True)  # Create folder if missing


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """Handles image upload and saves it in the uploads directory."""
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        img_path = os.path.join(UPLOAD_DIR, file.filename)
        img.save(img_path)
        return {"message": "Upload successful", "filePath": img_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/process/")
async def process_uploaded_image(file: UploadFile = File(...), operations: str = Form(...)):
    """Processes an uploaded image with transformations."""
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))

        ops = json.loads(operations)  # Parse JSON

        if "resize" in ops:
            width = ops["resize"]["width"]
            height = ops["resize"]["height"]
            img = resize_image(img, width, height)

        if "grayscale" in ops and ops["grayscale"]:
            img = img.convert("L")  # Convert to grayscale

        if "compress" in ops:
            quality = ops["compress"].get("quality", 50)
            img = compress_image(img, quality)

        if "rotate" in ops:
            degrees = ops["rotate"]
            img = rotate_image(img, degrees)

        if "filter" in ops:
            filter_type = ops["filter"]
            img = apply_filter(img, filter_type)

        if "thumbnail" in ops:
            img = create_thumbnail(img)

        if "mask" in ops and ops["mask"]:
            img = mask_image(img)

        processed_path = os.path.join(UPLOAD_DIR, "processed_image.png")
        img.save(processed_path)  # Save as PNG

        return {"message": "Processed successfully", "filePath": processed_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/load-from-url/")
async def load_image_from_url(image_url: str):
    """Loads an image from a URL and saves it locally."""
    print(f"Received URL: {image_url}")  # Debugging output
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        print(f"✅ Request successful: {response.status_code}")  # Debugging
        img = Image.open(io.BytesIO(response.content))
        img.save("downloaded_images/downloaded_image_from_url.jpg")  # Save locally
        return {"image_url": "http://127.0.0.1:8000/downloaded_images/downloaded_image_from_url.jpg"}
    except Exception as e:
        print(f"❌ Exception: {e}")  # Debugging
        raise HTTPException(status_code=500, detail=f"Failed to load image: {str(e)}")
