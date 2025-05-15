
import time
import pygame
import os
os.chdir("/home/prim/little-maestro")
from songs import songs

# Sound setup
# Initialize pygame mixer
pygame.mixer.init()

try:
    import serial
except ImportError:
    print("pyserial is not installed.") # pip install pyserial 
    serial = None

arduino = None
if serial:
    try:
        arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # check and update port number
        time.sleep(2)  # Give Arduino time to reset
        print("Connected to Arduino.")
    except serial.SerialException:
        print("Not connected to an Arduino.")

try:
    import Jetson.GPIO as GPIO
    from Jetson_MFRC522 import SimpleMFRC522
    reader = SimpleMFRC522()
except (ImportError, RuntimeError):
    print("Running on non-Jetson system")

tempo = 0.5
instrument = ["piano", "guitar", "violin", "flute"]
instrument_index = 0
current_instrument = instrument[instrument_index]
level_to_color = ["Green","Yellow","Red"]

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

card_to_song = {
    "64123d3d": "HBD",
    "9438b949": "Jingle Bells",
    "9449303d": "Canon",
}

def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = current_instrument + "_directory"
    file_path = os.path.join("little_maestro",instrument_folder, file_name)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"[INFO] Playing: {current_instrument} - {note}")
        time.sleep(tempo)  # Adjust delay based on tempo

    else:
        raise ValueError(f"play_note, Error: {file_path} not found!")


def play_song(song_name):
    if song_name not in songs:
        print(f"[Error] play_song, '{song_name}' not found!")
        return
    
    print(f"[INFO] play_song, Playing {song_name} with {current_instrument}")
    for note in songs[song_name]:
        play_note(note)
    print(f"[INFO] play_song, '{song_name}' ended")

def check_sequence(song_name, note_index):
    try:
        print(f"[INFO] check_sequence, checking note {note_index + 1} in {song_name}, {songs[song_name][note_index]}")
        while True:
            arduino.write(b'check note\n')
            line = arduino.readline().decode('utf-8').strip()

            if not line:
                time.sleep(0.1)
                continue

            if line.startswith("Note"):
                note_info = line.split()  # Split the note info (e.g., "Note CU)")

                if len(note_info) < 2:
                    raise ValueError(f"check_sequence, malformed note message: '{line}'")

                note = note_info[1]  # Get the note (e.g., "C")
                # Play the corresponding note sound
                led(note,level_to_color[level])
                play_note(note)
                led(note,"off")

                # Check correctness
                if note == songs[song_name][note_index]:
                    print("[INFO] check_sequence, 'Correct'")
                    return True
                elif line != songs[song_name][note_index]:
                    print("[INFO] check_sequence, 'Incorrect'")
                    return False
                
            else:
                print(f"[ERROR] check_sequence, unrecognized serial message: '{line}'")
    except Exception as e:
        print(f"[ERROR] check_sequence failed: {e}")

def led(led_name, color): # I for changing intruments, piano, guitar, violin, flute for instrument indicating LEDs
    leds = []
    try: 
        if led_name in instrument or led_name == 'I' or led_name == "record_stop":
            leds.append(led_name_to_id(led_name))

        elif len(led_name) < 2:
            raise ValueError(f"led, Invalid note format: '{led_name}'")

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



def detect_card():
    try:
        id, text = reader.read()
        song_name = text.strip()

        if id == 0:
            return
        
        print(f"[INFO] Card Detected: {song_name}")
        learning(song_name)

    except Exception as e:
        print(f"[ERROR] {e}")

def freestyle():
    global current_instrument, instrument_index
    led(current_instrument,"WHITE")
    try:
        arduino.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino.readline().decode('utf-8').strip()
        
        if line == "record_stop":
            record()
        
        elif line.startswith("Note"):
            note = line.split()[1]
            led(note,"WHITE")
            play_note(note)
            led(note,"off")

        elif line == "I":
            led(current_instrument,"off")
            if instrument_index == 3:
                instrument_index = 0
            else:
                instrument_index += 1
            current_instrument = instrument[instrument_index]
            led(current_instrument, "WHITE")
            print(f"[INFO] Change instrument to '{current_instrument}'")
        
        else:
            print(f"[ERROR] Unrecognized serial message: '{line}'")

    except Exception as e:
        print(f"[ERROR] {e}")

def record():
    global current_instrument, instrument_index
    recorded_song = []
    record = True
    playing = False
    while not playing:
        print("[INFO] Start recording")
        led("record_stop","red")
        while record:
            arduino.write(b'check note\n')  # Ask Arduino for pressed note
            recording_note_line = arduino.readline().decode('utf-8').strip()

            if not recording_note_line:
                time.sleep(0.1)

            elif recording_note_line.startswith("Note"):
                note = recording_note_line.split()[1]
                recorded_song.append(note)
                led(note,"WHITE")
                play_note(note)
                led(note,"off")

            elif recording_note_line == "I":
                led(current_instrument,"off")
                if instrument_index == 3:
                    instrument_index = 0
                else:
                    instrument_index += 1
                current_instrument = instrument[instrument_index]
                led(current_instrument, "WHITE")
                print(f"Change instrument to '{current_instrument}'")
            
            elif recording_note_line == ("record_stop"):
                record = False
                print("[INFO] Stop recording")
                led("record_stop","yellow") # indicates that there is a recorded song 

            else:
                print(f"[INFO] Unrecognized serial message: '{recording_note_line}'")

        arduino.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino.readline().decode('utf-8').strip()

        if not line:
            time.sleep(0.1)

        elif line.startswith("Note"):
            note = line.split()[1]
            led(note,"WHITE")
            play_note(note)
            led(note,"off")
        
        elif recording_note_line == "I":
            led(current_instrument,"off")
            if instrument_index == 3:
                instrument_index = 0
            else:
                instrument_index += 1
            current_instrument = instrument[instrument_index]
            led(current_instrument, "BLUE")
            print(f"Change instrument to '{current_instrument}'")

        elif line == ("record_stop"):
            playing = True
            print("[INFO] Start playing recorded song")
            led("record_stop","green")

        else:
            print(f"[ERROR] record, Unrecognized serial message: '{line}'")

    for notes in recorded_song:
        play_note(notes)
    led("record_stop","off")
    print("return to freestyle mode")

def learning(song_name):
    global level
    level = 1
    print("[MODE] Learning Mode")
    if song_name in songs:
        print(f"[INFO] Learning {song_name}")
        file_path = os.path.join(f"{song_name}-speech.mp3")
        if os.path.exists(file_path):
            pygame.mixer.Sound(file_path).play()
            time.sleep(2)

        while level <= 3:

            # ======== LEVEL 1 ========
            if level == 1:
                print('Level 1')
                file_path = os.path.join(f"level-{level}.mp3")
                if os.path.exists(file_path):
                    pygame.mixer.Sound(file_path).play()
                    time.sleep(2)
                else:
                    print(f"{file_path} not found")

                success=True
                while True:
                    for i in range(len(songs[song_name])):
                        led(songs[song_name][i+1],"GREEN")
                        play_note(songs[song_name][i+1])
                        led(songs[song_name][i+1],"off")
                        result=check_sequence(song_name, i)
                        if not result:
                            success = False
                            break
                    if success:
                        level = 2
                        print("[LEVEL 1] Complete! Moving to level 2.")
                        break
                    if not success:
                        print("[LEVEL 1] Wrong note, restarting level 1.")
                        level = 1
                        break

                
        #===== LEVEL 2 =====
            if level == 2:
                print('Level 2')
                file_path = os.path.join(f"level-{level}.mp3")
                if os.path.exists(file_path):
                    pygame.mixer.Sound(file_path).play()
                    time.sleep(2)
                else:
                    print(f"{file_path} not found")

                success = True
                while True:
                    for i in range(len(songs[song_name])):
                        led(songs[song_name][i+1],"Yellow")
                        play_note(songs[song_name][i+1])
                        led(songs[song_name][i+1],"off")
                    for i in range(len(songs[song_name])):
                        result = check_sequence(song_name, i)
                        if not result:
                            success = False
                            break
                    if success:
                        level = 3
                        print("[LEVEL 2] Complete! Moving to level 3.")
                        break
                    if not success:
                        print("[LEVEL 2] Wrong note, restarting level 2.")
                        level = 2
                        break
    #===== LEVEL 3 =====
            if level == 3:
                print('Level 3')
                file_path = os.path.join(f"level-{level}.mp3")
                if os.path.exists(file_path):
                    pygame.mixer.Sound(file_path).play()
                    time.sleep(2)
                else:
                    print(f"{file_path} not found")

                success = True
                play_song(song_name)
                while True:
                    for i in range(len(songs[song_name])):
                        result = check_sequence(song_name, i)
                        if not result:
                            success = False
                            break
                    if success:
                        level = 4
                        print("[LEVEL 3] Congratulation! Learning mode Completed! enter freestyle mode")
                        break
                    if not success:
                        print("[LEVEL 3] Wrong note, restarting level 2.")
                        level = 2
                        break
