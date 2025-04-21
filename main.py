import serial
import pygame
import time
import os
import RPi.GPIO as GPIO
from Jetson_MFRC522 import SimpleMFRC522

from functions import check_sequence, led, play_note_instrument, detect_card, freestyle, learning, play_song

# Initialize RFID reader
reader = SimpleMFRC522()

# Initialize Serial Communication with Arduino (Change port if needed)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Give Arduino time to reset

# Initialize Pygame for Sound
pygame.mixer.init()


# Defaults
current_mode = "freestyle"  # Default mode
current_instrument = "piano"  # Default instrument

# Paths for sound files
PIANO_SOUND_DIR = 'piano-mp3'

#main loop
while True:
    print("[STATE] Waiting for card...")
    try:
        id, text = reader.read()  # Blocking call
        song_name = text.strip()
        learning(song_name)
    except Exception:
        print("[INFO] No card detected, going Freestyle.")
        freestyle()

    time.sleep(0.5)

