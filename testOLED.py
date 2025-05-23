from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

image_path = "/home/prim/Downloads/pixelfroggy-01.png"
image = Image.open(image_path).resize((128, 64)).convert("1")
device.image(image)
device.show()