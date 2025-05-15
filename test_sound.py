
import time
import pygame
import os
pygame.mixer.init()

def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = "piano" + "_directory"
    file_path = os.path.join(instrument_folder, file_name)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"[INFO] Playing: Piano - {note}")
        time.sleep(0.5)  # Adjust delay based on tempo

    else:
        raise ValueError(f"play_note, Error: {file_path} not found!")


#from songs import songs

def play_song(song_name):
    print(f"[INFO] Playing song: {song_name}")
    for note in songs[song_name]:
        try:
            play_note(note)
        except ValueError as e:
            print(e)

level = 1
file_path = os.path.join(f"level-{level}.mp3")
if os.path.exists(file_path):
    pygame.mixer.Sound(file_path).play()
    time.sleep(2)
play_note("C4")

#play_song('HBD')