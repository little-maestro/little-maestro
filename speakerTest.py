import time
import pygame
pygame.mixer.init()
import os
os.chdir(".")

tempo = 0.5

def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = "xylo" + "_directory"
    file_path = os.path.join(instrument_folder, file_name)
    print(file_path)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"[INFO] Playing: piano - {note}")
        time.sleep(tempo)  # Adjust delay based on tempo

    else:
        raise ValueError(f"play_note, Error: {file_path} not found!")

play_note('G3')
