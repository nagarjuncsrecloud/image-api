# Description:              Dockerfile is specifically used to containerize a Python/FastAPI application for backend using "Uvicorn" and deploy it in a lightweight, portable, and scalable manner.
# Purpose:                  To containerize a FastAPI application and deploy since FastAPI + Uvicorn is great for high-performance APIs. 
# File Name:                Dockerfile
# File Type:                Plain text (text/plain)
# Installations:            Docker, Docker Desktop, Pip
# Functions (Re-Usable):    None.
# Note:                     Docker automatically detects Dockerfile without needing an extension. However, if you have multiple Dockerfiles, you can name them differently (e.g., Dockerfile.dev, Dockerfile.prod)
# Author:                   Nagarjun Gutha Chandrasekaran
# Date:                     02/26/2025
# Version:                  1.0
# Modifications:

# Use the official Python 3.9 base image
FROM python:3.9  

# Set the working directory inside the container to /app
WORKDIR /app  

# Copy the requirements.txt file from the host machine to the container
COPY docker/requirements.txt .  

# Install dependencies listed in requirements.txt using pip
RUN pip install -r requirements.txt  

# Explicitly install uvicorn in case it's missing
RUN pip install uvicorn fastapi

# Copy all files from the current directory to the container’s working directory
COPY app /app  

RUN mkdir -p /app/uploads /app/downloaded_images
RUN chmod -R 777 /app/uploads /app/downloaded_images
RUN chown -R 1000:1000 /app/uploads /app/downloaded_images

# Set a non-root user
USER 1000 

# Command to start the FastAPI app using Uvicorn
CMD ["sh", "-c", "PYTHONPATH=/app uvicorn main:app --host 0.0.0.0 --port 8000"]
# main:app → Looks for app inside main.py.
# 0.0.0.0 → Listens on all network interfaces.
# Port 8000 → The application will run on port 8000.
