import serial
import pygame
import time
import os
import RPi.GPIO as GPIO
from Jetson_MFRC522 import SimpleMFRC522

from functions import check_sequence, led
from little_maestro_sound import play_note_instrument
from songs import play_song
from song_card import detect_card
from modes import freestyle, learning, switch_to_learning, switch_to_freestyle

# Initialize RFID reader
reader = SimpleMFRC522()

# Initialize Serial Communication with Arduino (Change port if needed)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Give Arduino time to reset

# Initialize Pygame for Sound
pygame.mixer.init()

# Defaults
current_mode = "freestyle"  # Default mode
instrument = "piano"  # Default instrument

# Paths for sound files
PIANO_SOUND_DIR = 'piano-mp3'
    

def listen_to_buttons():
    """Continuously listens for button presses from Arduino and responds accordingly."""
    global mode

    while True:
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()

            if line.startswith("Mode"):
                _, mode = line.split()
                current_mode = mode
                print(f"Mode switched to: {current_mode}")

            elif line.startswith("Note"):
                _, note = line.split()
                handle_note_input(note)

def handle_note_input(note):
    """Handles what happens when a button is pressed, depending on the mode."""
    if current_mode == "freestyle":
        play_note_instrument(note, instrument)

    elif current_mode == "learning":
        # Example: Hardcoded song for now, but should be dynamic later
        song_name = "HBD"
        note_index = 0  # This should track user progress in the song

        check_sequence(song_name, note_index)

        # Update LED to show next note to press
        next_note_led = note_index + 1
        if next_note_led < len(songs[song_name]):
            led(next_note_led, "blue")

def main():
    """Main function to start the game."""
    print("Smart Music Toy Started!")
    freestyle() #starts in freestyle mode

if __name__ == "__main__": #main program loop
    freestyle_mode()

    