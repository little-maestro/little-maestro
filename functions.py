import serial
import time
import pygame
import os

# Sound setup
# Initialize pygame mixer
pygame.mixer.init()
# Set the path to the downloaded sound files (make sure it's correct and path uses forward slashes or raw strings)
PIANO_SOUND_DIR = 'piano-mp3'  # Update path to only point to the root folder (piano-mp3)
# Define a dictionary for mapping instruments to specific folders or sound sets
instrument_map = {
    "piano": ''
}

instrument = ["piano", "guitar", "ranad", "klui"]
instrument_index = 0
current_instrument = instrument[instrument_index]

def change_instrument():
    try:
        while True:
            arduino.write(b'check note\n')
            line = arduino.readline().decode('utf-8').strip()

            if not line:
                continue

            if not line.startswith("Note"):

                if len(line) > 1:
                    raise ValueError(f"Malformed command message: '{line}'")

                if line == "I":
                    if instrument_index == 3:
                        instrument_index = 0
                    else:
                        instrument_index += 1
                    current_instrument = instrument[instrument_index]
                    print(f"Change instrument to '{current_instrument}'")
                    return
                elif line == "o":
                    print('New feature activated')
                    return
                
            else:
                print(f"[INFO] Unrecognized serial message: '{line}'")

    except Exception as e:
        print(f"[ERROR] check_sequence failed: {e}")

note_to_led = {
    "C": 5,
    "C#": 6,
    "D": 7,
    "D#": 8,
    "E": 9,
    "F": 10,
    "F#": 11,
    "G": 12,
    "G#": 13,
    "A": 14,
    "A#": 15,
    "B": 16
}

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

# Serial communication setup (change the port if needed)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Give Arduino time to reset


def check_sequence(song_name, note_sequence):
    try:
        while True:
            arduino.write(b'check note\n')
            line = arduino.readline().decode('utf-8').strip()

            if not line:
                continue

            if line.startswith("Note"):
                note_info = line.split()  # Split the note info (e.g., "Note CU)")

                if len(note_info) < 2:
                    raise ValueError(f"Malformed note message: '{line}'")

                note = note_info[1]  # Get the note (e.g., "C")
                # Play the corresponding note sound
                play_note_instrument(note, instrument)

                # Check correctness
                if note == songs[song_name][note_sequence]:
                    print('Corect')
                    return
                elif line != songs[song_name][note_sequence]:
                    print('Incorrect')
                    return
                
            else:
                print(f"[INFO] Unrecognized serial message: '{line}'")
    except Exception as e:
        print(f"[ERROR] check_sequence failed: {e}")

def led(note_str, color): # I for changing intruments, Piano, Guitar, Ranad, Klui for instrument indicating LEDs
    leds = []

    try: 
        if note_str == "I":
            leds = [20]  # Instrument change
        elif note_str.lower() == "piano":
            leds = [1]
        elif note_str.lower() == "guitar":
            leds = [2]
        elif note_str.lower() == "ranad":
            leds = [3]
        elif note_str.lower() == "klui":
            leds = [4]
        else:
            if len(note_str) < 2:
                raise ValueError(f"Invalid note format: '{note_str}'")
            
            pitch = note_str[:-1]  # Extract note name, e.g., "C", "C#"
            octave = note_str[-1]  # Extract octave digit

            if pitch not in note_to_led:
                raise ValueError(f"Unknown pitch: '{pitch}'")
            
            if octave not in ('3', '4', '5'):
                raise ValueError(f"Unsupported octave: '{octave}'")
            
            # Add corresponding LEDs
            leds.append(note_to_led[pitch])
            if octave == '3':
                leds.append(19)
            elif octave == '5':
                leds.append(18) #18 is led number
        
        # Send command if we have valid LED ids
        if leds:
            ids = ",".join(str(i) for i in leds)
            command = f"LED {ids} {color.upper()}\n"
            arduino.write(command.encode('utf-8'))
            print(f"Sent: {command.strip()}")
        else:
            print("No valid LEDs determined from input.")

    except Exception as e:
        print(f"[ERROR] LED command failed for '{note_str}': {e}")


import RPi.GPIO as GPIO
import sys
from Jetson_MFRC522 import SimpleMFRC522

reader = SimpleMFRC522()
print("Place your RFID card...")
try:
    id, text = reader.read()
    print(f"ID: {id}, Text: {text}")
finally:
    GPIO.cleanup()


def detect_card():
    global mode
    print("Insert card")
    
    try:
        id, text = reader.read()
        song_name = text.strip()
        print(f"Card Detected: {song_name}")

        if song_name in songs:
            learning_mode(song_name)
        else:
            print(f"[ERROR] Song '{song_name}' not found! Returning to freestyle.")
            mode = "freestyle"

    finally:
        GPIO.cleanup()  # Clean up GPIO to prevent issues

def freestyle():
    global mode
    print("[MODE] Freestyle Mode")
    while True:
        arduino.write(b'get_note\n')  # Ask Arduino for pressed note
        line = arduino.readline().decode('utf-8').strip()
        
        if line == "CARD_DETECTED":  
            return detect_card()  # Switch mode if a card is detected
        
        if line.startswith("Note"):
            note = line.split()[1]
            play_note(note)

def learning():
    print("[MODE] Learning Mode")
    arduino.write(b'get_song_name\n')  # Request song name from arduino !!! fixxxxx
    song_name = arduino.readline().decode('utf-8').strip()

    if song_name in songs:
        print(f"[INFO] Learning {song_name}")
        check_sequence(song_name, note_sequence=)  # Start guiding user through the song
    else:
        print("[ERROR] Invalid song detected")
        switch_to_freestyle()