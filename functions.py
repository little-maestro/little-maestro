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
                leds.append(18)
        
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
