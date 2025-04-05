import pygame
import time
import os

pygame.mixer.init()

songs = {
    "HBD": ["G3", "G3", "A3","G3", "C4", "B3", "G3", "G3", "A3", "G3", "D4", "C4",
            "G3", "G3", "G4", "E4", "C4", "B3", "A3", "F4", "F4", "E4", "C4", "D4", "C4"],

    "Jingle Bells": ["E4", "E4", "E4", "E4", "E4", "E4", "E4", "G4", "C4", "D4", "E4",
                     "F4", "F4", "F4", "F4", "F4", "E4", "E4", "E4", "E4", 
                     "E4", "D4", "D4", "E4", "D4", "G4",
                     "E4", "E4", "E4", "E4", "E4", "E4", "E4", "G4", "C4", "D4", "E4",
                     "F4", "F4", "F4", "F4", "F4", "E4", "E4", "E4", "E4", 
                     "G4", "G4", "F4", "D4", "C4"]
}

instrument_map = {"piano": ""}

PIANO_SOUND_DIR = 'piano-mp3'

def play_song(song_name, instrument, tempo):
    if song_name not in songs:
        print("Song not found!")
        return

    for note in songs[song_name]:
        file_path = os.path.join(PIANO_SOUND_DIR, instrument_map[instrument], f"{note}.mp3")
        
        if os.path.exists(file_path):
            pygame.mixer.Sound(file_path).play()
            print(f"Playing: {note}")
            time.sleep(tempo)  # Adjust delay based on tempo

        else:
            print(f"Error: {file_path} not found!")

play_song("HBD", "piano", 0.4)
