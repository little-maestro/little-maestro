import Jetson.GPIO as GPIO
import spidev
import time
from mfrc522 import SimpleMFRC522

# Set up GPIO mode (BCM refers to GPIO pin numbering)
GPIO.setmode(GPIO.BCM)

# Set up the GPIO pins for MFRC522
GPIO.setup(7, GPIO.OUT)  # RST Pin (reset pin, connected to GPIO 7, physical pin 26)
GPIO.setup(8, GPIO.OUT)  # CS Pin (Chip Select, connected to GPIO 8, physical pin 24)

# Initialize SPI (using SPI0, bus 0, device 0)
spi = spidev.SpiDev()
spi.open(0, 0)  # Use SPI bus 0, device 0 (SPI0)
spi.max_speed_hz = 50000  # SPI speed, you can adjust this as needed
spi.mode = 0b00  # SPI Mode 0 (CPOL=0, CPHA=0)

# Initialize the MFRC522 reader
reader = SimpleMFRC522()

# Example loop to read an RFID tag
try:
    while True:
        print("Place your tag near the reader...")
        id, text = reader.read()  # Read RFID tag
        print(f"ID: {id}, Text: {text}")
        time.sleep(1)

finally:
    GPIO.cleanup()  # Clean up GPIO settings
    spi.close()     # Close the SPI connection
