
import time
import pygame
import os

def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = "piano" + "_directory"
    file_path = os.path.join("little-maestro",instrument_folder, file_name)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"[INFO] Playing: Piano - {note}")
        time.sleep(0.5)  # Adjust delay based on tempo

    else:
        raise ValueError(f"play_note, Error: {file_path} not found!")
    

level = 1
file_path = os.path.join("little-maestro",f"level-{level}.mp3")
if os.path.exists(file_path):
    pygame.mixer.Sound(file_path).play()
    time.sleep(2)
play_note("C4")