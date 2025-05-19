from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image

# Initialize I2C and OLED
serial = i2c(port=1, address=0x3C)  # Common I2C address
device = ssd1306(serial, width=128, height=64)

# Load and display one image
image_path = "/home/prim/Downloads/pixelfroggy-01.png" 
image = Image.open(image_path).resize((128, 64)).convert("1")
device.display(image)