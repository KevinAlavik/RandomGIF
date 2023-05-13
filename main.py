import base64
import glob
import io
import os
import random
import string
from PIL import Image
import numpy as np
from urllib.request import urlopen
import sys

def generate_random_image(width, height):
    # Generate random pixel data
    pixels = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)

    # Create PIL image from pixel data
    image = Image.fromarray(pixels)

    # Create an in-memory buffer to hold the image data
    buffer = io.BytesIO()

    # Save the image to the buffer in JPEG format
    image.save(buffer, format='JPEG')

    # Encode the image data as base64
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Generate a random string for the image name
    image_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create the data URL string
    data_url = f"data:image/jpeg;base64,{encoded_image}"

    return image_name, data_url


# Create "images" directory if it doesn't exist
os.makedirs("images", exist_ok=True)

num_iterations = int(sys.argv[1]) if len(sys.argv) > 1 else 60

for _ in range(num_iterations):
    width = 100
    height = 100
    image_name, data_url = generate_random_image(width, height)
    print(data_url)

    # Fetch the image data using urlopen
    response = urlopen(data_url)
    image_data = response.read()

    # Save the image with a random filename in the "images" directory
    file_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".jpg"
    file_path = os.path.join("images", file_name)
    with open(file_path, "wb") as image_file:
        image_file.write(image_data)

# Get all JPEG files in the "images" directory
image_files = glob.glob("images/*.jpg")

# Create a list to store the images
images = []
for file_path in image_files:
    image = Image.open(file_path)
    images.append(image)

# Save the images as an animated GIF
gif_file_path = "images/animated.gif"
images[0].save(
    gif_file_path,
    save_all=True,
    append_images=images[1:],
    duration=200,
    loop=0
)

# Remove individual JPEG files
for file_path in image_files:
    os.remove(file_path)