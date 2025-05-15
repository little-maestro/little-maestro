#run this on terminal in jetson
#sudo apt update
#sudo apt install python3-pip
#pip3 install luma.oled pillow

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image
import time
import os

# Setup OLED
serial = i2c(port=1, address=0x3C)  # Most OLEDs use 0x3C
device = ssd1306(serial, width=128, height=64)

# Folder containing images
image_folder = "/home/jetson/oled_images"

# Get list of BMP files
image_files = [f for f in os.listdir(image_folder) if f.endswith(".bmp")]
image_files.sort()  # Optional: sort filenames alphabetically


#case 1: jump when congrats = 4 pictures -> loop 7 steps from down -> up -> down
# Display each image one by one
for image_file in image_files:
    path = os.path.join(image_folder, image_file)
    image = Image.open(path).convert("1")  # Convert to 1-bit black & white
    device.display(image)
    time.sleep(2)  # Delay 2 seconds between images

#case 2: if incorrectly press -> sad frog
# Load frog image and convert to 1-bit (black and white)
image = Image.open("/home/jetson/oled_images/frog.bmp").convert("1")
# Display image on OLED
device.display(image)


#for png
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import os
import time

serial = i2c(port=1, address=0x3C)  # adjust if your OLED uses a different I2C address or port
device = ssd1306(serial)


#case 1 
image_folder = "/home/jetson/oled_images"  # replace with your actual path
png_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".png")])


for file_name in png_files:
    file_path = os.path.join(image_folder, file_name)
    # Load image, resize to 128x64, convert to 1-bit black & white
    image = Image.open(file_path).resize((128, 64)).convert("1")
    # Display image on OLED
    device.display(image)
    time.sleep(1)  # show for 1 second, adjust as needed


#case 2
image_path = "/home/jetson/oled_images/frog.png"  # replace with your actual path
image = Image.open(image_path).resize((128, 64)).convert("1")
device.display(image)
