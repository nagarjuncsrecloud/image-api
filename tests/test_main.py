import pytest
from fastapi.testclient import TestClient
from app.main import app
from PIL import Image
import io
import os
from unittest.mock import patch
import requests
from io import BytesIO

# Define absolute path to test image
#file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_images", "test.jpg"))

# Print the current working directory (for CI/CD debugging)
print(f"DEBUG: CI Current working directory: {os.getcwd()}")

# Define absolute path to test image
file_path = os.path.abspath(os.path.join(os.getcwd(), "tests", "test_images", "test.jpg"))

print(f"DEBUG: Checking path -> {file_path}")

assert os.path.exists(file_path), f"❌ Test image is missing at {file_path}!"

client = TestClient(app)

def test_upload_image():
    with open(file_path, "rb") as file:
        response = client.post("/upload/", files={"file": file})
    assert response.status_code == 200
    assert "Upload successful" in response.json()["message"]

def test_resize_image():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"resize": {"width": 200, "height": 200}}'})
    assert response.status_code == 200

def test_apply_grayscale():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"grayscale": true}'})
    assert response.status_code == 200

def test_apply_filter():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"filter": "sepia"}'})
    assert response.status_code == 200

def test_compress_image():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"compress": {"quality": 50}}'})
    assert response.status_code == 200

def test_rotate_image():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"rotate": 90}'})
    assert response.status_code == 200

def test_create_thumbnail():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"thumbnail": true}'})
    assert response.status_code == 200

def test_mask_image():
    with open(file_path, "rb") as file:
        response = client.post("/api/process/", files={"file": file}, data={"operations": '{"mask": true}'})
    assert response.status_code == 200

def create_test_image():
    """Generates an in-memory JPEG image."""
    img = Image.new("RGB", (100, 100), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    return img_bytes.getvalue()

@patch("app.main.requests.get")
def test_load_image_from_url(mock_get):
    print("Mocking requests.get")

    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = create_test_image()
    mock_response.raw = BytesIO(mock_response.content)

    response = client.get("/load-from-url/?image_url=https://dummyimage.com/600x400/000/fff")

    print("Mock called:", mock_get.called)
    print("Response status:", response.status_code)

    assert response.status_code == 200
