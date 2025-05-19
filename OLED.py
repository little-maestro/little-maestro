#run this on terminal in jetson
#sudo apt update
#sudo apt install python3-pip
#pip3 install luma.oled pillow



frog1 = https://drive.google.com/file/d/1J-9biZCHdiRsvZ7MyFPbuNQsD6VA4Rfb/view?usp=sharing
frog2 = https://drive.google.com/file/d/1ZrTEKBj7hJlBMvE_1V9-DyoFklNcoYUr/view?usp=sharing
frog3 = https://drive.google.com/file/d/1jbqmB4Xc87UumeIYW8amrNygzRJpRQKd/view?usp=sharing
frog4 = https://drive.google.com/file/d/1jbqmB4Xc87UumeIYW8amrNygzRJpRQKd/view?usp=sharing
frogsad = https://drive.google.com/file/d/1WsDy8PXQSfIGBOLyd9el9xSfVN2yaMCj/view?usp=sharing
level1 = https://drive.google.com/file/d/1lRePEYT_uSbFL8hRbslurkjaNwJBpDu_/view?usp=sharing
level2 = https://drive.google.com/file/d/1r5EFWqc3PhDq7jgsjzdnMUGKAYSPexzw/view?usp=sharing
level3 = https://drive.google.com/file/d/1s0N0fl-f89HbZJz9wVrpCRNmr6GDwycI/view?usp=sharing
canon = https://drive.google.com/file/d/1fRixtzjfV8RujqiJfTnAewm0xjL3Yrvt/view?usp=sharing
jb = https://drive.google.com/file/d/1fRixtzjfV8RujqiJfTnAewm0xjL3Yrvt/view?usp=sharing
hbd = https://drive.google.com/file/d/1Mmx3zJzd95VvDFi4mfnZkv7d-_dkJgao/view?usp=sharing

#for png
from PIL import Image
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
import os
import time

serial = i2c(port=1, address=0x3C)  # adjust if your OLED uses a different I2C address or port
device = ssd1306(serial)


#case 1: jump when congrats = 4 pictures -> loop 7 steps from down -> up -> down
image_folder = "/home/jetson/oled_images"  # replace with your actual path
png_files = sorted([f for f in os.listdir(image_folder) if f.endswith(".png")])

for file_name in png_files:
    file_path = os.path.join(image_folder, file_name)
    # Load image, resize to 128x64, convert to 1-bit black & white
    image = Image.open(file_path).resize((128, 64)).convert("1")
    # Display image on OLED
    device.display(image)
    time.sleep(1)  # show for 1 second, adjust as needed


#case 2: if incorrectly press -> sad frog
image_path = "/home/jetson/oled_images/frog.png"  # replace with your actual path
image = Image.open(image_path).resize((128, 64)).convert("1")
device.display(image)

