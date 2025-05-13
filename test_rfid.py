import Jetson.GPIO as GPIO
from mfrc522 import SimpleMFRC522

# Set up GPIO
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setwarnings(False)

# Initialize the MFRC522 reader
reader = SimpleMFRC522()

try:
    print("Place your RFID tag near the reader...")
    # Read RFID tag
    id, text = reader.read()
    
    # Print tag ID and text
    print(f"ID: {id}")
    print(f"Text: {text}")

finally:
    GPIO.cleanup()  # Clean up GPIO settings to avoid issues when done
