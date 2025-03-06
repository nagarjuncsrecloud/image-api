import pytest
from PIL import Image
import io
from app.image_processing import (
    resize_image, apply_filter, compress_image, rotate_image,
    create_thumbnail, mask_image, load_image_from_url
)

@pytest.fixture
def sample_image():
    """Create a sample in-memory image for testing."""
    img = Image.new("RGB", (300, 300), "blue")  # Create a blue image
    return img

def test_resize_image(sample_image):
    resized_img = resize_image(sample_image, 200, 200)
    assert resized_img.size == (200, 200)

def test_apply_grayscale(sample_image):
    gray_img = apply_filter(sample_image, "grayscale")
    assert gray_img.mode == "L"

def test_apply_sepia(sample_image):
    sepia_img = apply_filter(sample_image, "sepia")
    assert sepia_img.mode == "RGB"

def test_apply_blur(sample_image):
    blurred_img = apply_filter(sample_image, "blur")
    assert blurred_img is not None

def test_compress_image(sample_image):
    compressed_img = compress_image(sample_image, quality=10)
    assert isinstance(compressed_img, Image.Image)

def test_rotate_image(sample_image):
    rotated_img = rotate_image(sample_image, 90)
    assert rotated_img.size == (300, 300)  # Size should remain the same

def test_create_thumbnail(sample_image):
    thumbnail = create_thumbnail(sample_image)
    assert thumbnail.size[0] <= 100 and thumbnail.size[1] <= 100

def test_mask_image(sample_image):
    masked_img = mask_image(sample_image)
    assert masked_img.mode == "RGBA"

def test_load_image_from_url():
    img = load_image_from_url("https://c4.wallpaperflare.com/wallpaper/598/616/52/tv-show-dexter-s-laboratory-wallpaper-preview.jpg")
    assert isinstance(img, Image.Image)
