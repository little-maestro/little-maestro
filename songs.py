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

