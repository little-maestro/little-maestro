import serial
import pygame  # For sound playback

# Initialize Pygame mixer
pygame.mixer.init()

# Serial communication setup (change the port if needed)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

while True:
    line = arduino.readline().decode('utf-8').strip()
    if line:
        print("From Arduino:", line)

            # Play the corresponding note sound
            if note in notes_dict:
                print(f"Playing {note}...")
                pygame.mixer.music.load(notes_dict[note])  # Load the note sound
                pygame.mixer.music.play()  # Play the sound
            else:
                print(f"Unknown note: {note}")
        else:
            # Handle special buttons
            if line == 'o':
                print("Special command: o")
            elif line == 'I':
                print("Special command: I")
            elif line == 'Octave Up':
                print("Octave Up Command received")
            elif line == 'Octave Down':
                print("Octave Down Command received")