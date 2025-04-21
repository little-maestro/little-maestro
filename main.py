import pygame
import time

import Jetson.GPIO as GPIO
import atexit
atexit.register(GPIO.cleanup)

from functions import  detect_card, freestyle


# Initialize Pygame for Sound
pygame.mixer.init()


# Defaults
current_mode = "freestyle"  # Default mode
current_instrument = "piano"  # Default instrument

# Paths for sound files
PIANO_SOUND_DIR = 'piano-mp3'

#main loop
try:
    while True:
        freestyle()
        detect_card()
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    GPIO.cleanup()