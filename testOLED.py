import smbus

print("Scanning I2C buses for devices...")

for bus_num in range(9):  # Check i2c-0 to i2c-8
    try:
        bus = smbus.SMBus(bus_num)
        print(f"\nBus {bus_num}:")
        devices = []
        for addr in range(0x03, 0x78):
            try:
                bus.write_quick(addr)
                devices.append(hex(addr))
            except:
                continue
        if devices:
            print(" Devices found:", devices)
        else:
            print(" No devices found.")
    except FileNotFoundError:
        continue


'''
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image

serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

image_path = "/home/prim/Downloads/pixelfroggy-01.png"
image = Image.open(image_path).resize((128, 64)).convert("1")
device.image(image)
device.show()
'''