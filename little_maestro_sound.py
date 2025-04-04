import pygame
import time
import os

# Initialize pygame mixer
pygame.mixer.init()

# Set the path to the downloaded sound files (make sure it's correct and path uses forward slashes or raw strings)
PIANO_SOUND_DIR = 'piano-mp3'  # Update path to only point to the root folder (piano-mp3)

# Define a dictionary for mapping instruments to specific folders or sound sets
instrument_map = {
    "piano": ''
}

def play_note_instrument(note, instrument):
    if instrument not in instrument_map:
        print(f"Error: {instrument} not found in instrument map!")
        return

    file_name = f"{note}.mp3"
    instrument_folder = instrument_map[instrument]
    file_path = os.path.join(PIANO_SOUND_DIR, instrument_folder, file_name)
    
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"Playing {instrument} - {note}")
        time.sleep(2)  # <-- This is essential to keep the sound playing
    else:
        print(f"Error: {file_path} not found!")

play_note_instrument("Gb5", "piano") 


