pip install pygame
import pygame
import os

# Initialize pygame mixer
pygame.mixer.init()

# Set the path to the downloaded sound files (make sure it's correct and path uses forward slashes or raw strings)
SOUND_DIR = 'piano-mp3'  # Update path to only point to the root folder (piano-mp3)

# Define a dictionary for mapping instruments to specific folders or sound sets
instrument_map = {
    "piano": "",  # No need to add the 'piano' folder again here
}

def play_note_instrument(note, instrument):
   
    # Ensure instrument is in the map
    if instrument not in instrument_map:
        print(f"Error: {instrument} not found in instrument map!")
        return

    # Build the file name with the note
    file_name = f"{note}.mp3"
    
    # Map instrument to folder and form the file path
    instrument_folder = instrument_map[instrument]
    file_path = os.path.join(SOUND_DIR, instrument_folder, file_name)
    
    # Check if the file exists before playing
    if os.path.exists(file_path):
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        print(f"Playing {instrument} - {note}")
    else:
        print(f"Error: {file_path} not found!")

# Example Usage
play_note_instrument("A5", "piano")  # Plays A5.mp3 from the piano folder
