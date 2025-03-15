from PIL import Image
import os

def create_dummy_image():
    os.makedirs("test_images", exist_ok=True)
    img = Image.new("RGB", (600, 400), color="black")
    img.save("test_images/test.jpg")

if __name__ == "__main__":
    create_dummy_image()
