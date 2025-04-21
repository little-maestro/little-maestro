# Install necessary libary (code from chat gpt in docs)

from Jetson_MFRC522 import SimpleMFRC522
import time
import Jetson.GPIO as GPIO

# Initialize the RFID reader
reader = SimpleMFRC522()

try:
    print("Place your RFID card to write text...")
    
    # Read the ID (just to check if the card is there)
    id, text = reader.read()
    print(f"ID: {id}, Text: {text}")

    # Ask the user to enter the text to write to the card
    song_name = input("Enter the song name to write on the card: ")

    # Write the new text to the card
    print("Writing to the card...")
    reader.write(song_name)
    print(f"Text '{song_name}' written to the card.")

finally:
    GPIO.cleanup()  # Clean up the GPIO when donev