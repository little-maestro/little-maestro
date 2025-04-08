#add to terminal
#sudo apt update  
#sudo apt install python3-pip  
#pip3 install spidev mfrc522

import RPi.GPIO as GPIO
import sys
from Jetson_MFRC522 import SimpleMFRC522

reader = SimpleMFRC522()
print("Place your RFID card...")
try:
    id, text = reader.read()
    print(f"ID: {id}, Text: {text}")
finally:
    GPIO.cleanup()





def detect_card():
    global mode
    print("Insert card")
    
    try:
        id, text = reader.read()
        song_name = text.strip()
        print(f"Card Detected: {song_name}")

        if song_name in songs:
            learning_mode(song_name)
        else:
            print(f"[ERROR] Song '{song_name}' not found! Returning to freestyle.")
            mode = "freestyle"

    finally:
        GPIO.cleanup()  # Clean up GPIO to prevent issues