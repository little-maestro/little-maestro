from Jetson_MFRC522 import SimpleMFRC522
import time

# Initialize the reader
reader = SimpleMFRC522()

try:
    print("Place your RFID card...")
    id, text = reader.read()
    print(f"ID: {id}, Text: {text}")
except Exception as e:
    print(f"Error: {e}")
