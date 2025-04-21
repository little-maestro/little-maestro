import serial
import time
import pygame
import os

from songs import songs

# Sound setup
# Initialize pygame mixer
pygame.mixer.init()

# Serial communication setup (change the port if needed)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Give Arduino time to reset



tempo = 10
instrument = ["piano", "guitar", "violin", "flute"]
instrument_index = 0
current_instrument = instrument[instrument_index]

led_name_to_id = {
    "piano": 1,
    "guitar": 2,
    "violin": 3,
    "flute": 4,
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
    "B": 16,
    "record_stop": 17,
    "up": 18,
    "down": 19,
    "I": 20
}

def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = current_instrument + "_directory"
    file_path = os.path.join(instrument_folder, file_name)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"Playing: {current_instrument} - {note}")
        time.sleep(tempo)  # Adjust delay based on tempo

    else:
        print(f"Error: {file_path} not found!")


def play_song(song_name):
    if song_name not in songs:
        print("Song not found!")
        return

    for note in songs[song_name]:
        play_note(note)


def check_sequence(song_name, note_index):
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
                play_note(note)

                # Check correctness
                if note == songs[song_name][note_index]:
                    print('Correct')
                    return
                elif line != songs[song_name][note_index]:
                    print('Incorrect')
                    return
                
            else:
                print(f"[INFO] Unrecognized serial message: '{line}'")
    except Exception as e:
        print(f"[ERROR] check_sequence failed: {e}")

def led(led_name, color): # I for changing intruments, Piano, Guitar, Ranad, Klui for instrument indicating LEDs
    leds = []

    try: 
        if led_name in instrument or led_name == 'I' or led_name == "record_stop":
            leds.append(led_name_to_id(led_name))

        elif len(led_name) < 2:
            raise ValueError(f"Invalid note format: '{led_name}'")

        else: 
            pitch = led_name[:-1]  # Extract note name, e.g., "C", "C#"
            octave = led_name[-1]  # Extract octave digit

            if pitch not in led_name_to_id:
                raise ValueError(f"Unknown pitch: '{led_name} -- {pitch}'")
            
            if octave not in ('3', '4', '5'):
                raise ValueError(f"Unsupported octave: '{led_name} -- {octave}'")
            
            # Add corresponding LEDs
            leds.append(led_name_to_id[pitch])
            if octave == '3':
                leds.append(led_name_to_id("down"))
            elif octave == '5':
                leds.append(led_name_to_id("up")) #18 is led number
        
        # Send command if we have valid LED ids
        if leds:
            ids = ",".join(str(i) for i in leds)
            command = f"LED {ids} {color.upper()}\n"
            arduino.write(command.encode('utf-8'))
            print(f"Sent: {command.strip()}")
        else:
            print("No valid LEDs determined from input.")

    except Exception as e:
        print(f"[ERROR] LED command failed for '{led_name}': {e}")


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
            learning(song_name)
        else:
            print(f"[ERROR] Song '{song_name}' not found! Returning to freestyle.")
            mode = "freestyle"

    finally:
        GPIO.cleanup()  # Clean up GPIO to prevent issues

def freestyle():
    global mode

    try:
        arduino.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino.readline().decode('utf-8').strip()
        
        if not line:
            time.sleep(0.5)

        elif line == "record_stop":
            record()
        
        elif line.startswith("Note"):
            note = line.split()[1]
            play_note(note)
        
        elif line == "I":
            if instrument_index == 3:
                instrument_index = 0
            else:
                instrument_index += 1
            current_instrument = instrument[instrument_index]
            led(current_instrument, "WHITE")
            print(f"Change instrument to '{current_instrument}'")
        
        else:
            print(f"[INFO] Unrecognized serial message: '{line}'")

    except Exception:
        print("[INFO] some error.")

def record():
    recorded_song = []
    record = True
    playing = False
    led()
    while not playing:
        while record:
            arduino.write(b'check note\n')  # Ask Arduino for pressed note
            recording_note_line = arduino.readline().decode('utf-8').strip()

            if not recording_note_line:
                time.sleep(0.5)

            elif recording_note_line.startswith("Note"):
                note = recording_note_line.split()[1]
                recorded_song.append(note)
                play_note(note)
                
            elif recording_note_line == ("record_stop"):
                record = False
                print("[INFO] Stop recording")
            
            elif recording_note_line == "I":
                if instrument_index == 3:
                    instrument_index = 0
                else:
                    instrument_index += 1
                current_instrument = instrument[instrument_index]
                led(current_instrument, "WHITE")
                print(f"Change instrument to '{current_instrument}'")

            else:
                print(f"[INFO] Unrecognized serial message: '{recording_note_line}'")

        arduino.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino.readline().decode('utf-8').strip()

        if not line:
            time.sleep(0.5)
        elif line.startswith("Note"):
            note = line.split()[1]
            play_note(note)
        
        elif line == ("record_stop"):
            playing = True
            print("[INFO] Start playing recorded song")
        
        elif recording_note_line == "I":
            if instrument_index == 3:
                instrument_index = 0
            else:
                instrument_index += 1
            current_instrument = instrument[instrument_index]
            led(current_instrument, "WHITE")
            print(f"Change instrument to '{current_instrument}'")

        else:
            print(f"[INFO] Unrecognized serial message: '{line}'")

    for notes in recorded_song:
        play_note(notes)

def learning(song_name):
    print("[MODE] Learning Mode")

    if song_name in songs:
        print(f"[INFO] Learning {song_name}")

        # ======== LEVEL 1 ========
        print('Level 1')
        while True:
            success=True
            for i in range(len(songs[song_name])):
                led_command = f"LED {i+1} GREEN\n" 
                arduino.write(led_command.encode())
                result=check_sequence(song_name, i)
                if not result:
                    print("[LEVEL 1] Wrong note, restarting level.")
                    success = False
                    break
            if success:
                print("[LEVEL 1] Complete! Moving to level 2.")
                break
                
    #===== LEVEL 2 =====
        play_song(song_name)
        while True:
            success = True
            for i in range(len(songs[song_name])):
                led_command = f"LED {i+1} BLUE\n"
                arduino.write(led_command.encode())
                result = check_sequence(song_name, i)
                if not result:
                    print("[LEVEL 2] Wrong note, restarting level.")
                    success = False
                    break
            if success:
                print("[LEVEL 2] Complete! Moving to level 3.")
                break
    #===== LEVEL 3 =====
        play_song(song_name)
        while True:
            success=True
            for i in range(len(songs[song_name])):
                result=check_sequence(song_name,i)
                if not result:
                    print("[LEVEL 3] Wrong note, restarting level.")
                    success = False
                    break
            if success:
                print("Congratulations")
                return

    else:
        print("[ERROR] Invalid song detected")