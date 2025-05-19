import time
import pygame
pygame.mixer.init()
import os
os.chdir("/home/prim/little-maestro")

try:
    import serial
except ImportError:
    print("pyserial is not installed.") # pip install pyserial 
    serial = None

arduino1 = None
arduino2 = None
if serial:
    try: 
        #check and update port number
        arduino1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1) # Button
        arduino2 = serial.Serial('/dev/ttyUSB1', 9600, timeout=1) # Card Reader
        time.sleep(2)  # Give Arduino time to reset
        print("Connected to Arduino.")
    except serial.SerialException:
        print("Not connected to an Arduino.")


tempo = 1
instrument = ["piano", "xylophone", "violin", "flute"]
instrument_index = 0
current_instrument = instrument[instrument_index]

songs = {
        "HBD": ["G3", "G3", "A3","G3", "C4", "B3", "G3", "G3", "A3", "G3", "D4", "C4",
                "G3", "G3", "G4", "E4", "C4", "B3", "A3", "F4", "F4", "E4", "C4", "D4", "C4"],

        "Jingle_Bells": ["E4", "E4", "E4", "E4", "E4", "E4", "E4", "G4", "C4", "D4", "E4",
                     "F4", "F4", "F4", "F4", "F4", "E4", "E4", "E4", "E4", 
                     "E4", "D4", "D4", "E4", "D4", "G4",
                     "E4", "E4", "E4", "E4", "E4", "E4", "E4", "G4", "C4", "D4", "E4",
                     "F4", "F4", "F4", "F4", "F4", "E4", "E4", "E4", "E4", 
                     "G4", "G4", "F4", "D4", "C4"],
        "Canon": [ "A5", "F#5", "G5", "A5", "F#5", "G5", "A5", "A4", 
                  "B4", "C#5", "D5", "E5", "F#5", "G5", "F#5", "D5", 
                  "E5", "F#5", "F#4", "G4", "A4", "B4", "A4", "G4", 
                  "A4", "F#4", "G4", "A4", "G4", "B4", "A4", "G4", 
                  "F#4", "E4", "F#4", "E4", "D4", "E4", "F#4", "G4", 
                  "A4", "B4", "G4", "B4", "A4", "B4", "C#5", "D5",  
                  "A4", "B4", "C#5", "D5", "E5", "F#5", "G5", "A5"]
}

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
    "9438b949": "Jingle-Bells",
    "9449303d": "Canon",
}

def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = current_instrument + "_directory"
    file_path = os.path.join(instrument_folder, file_name)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"[INFO] Playing: {current_instrument} - {note}")
        time.sleep(tempo)  # Adjust delay based on tempo

    else:
        raise ValueError(f"play_note, Error: {file_path} not found!")

def check_sequence(song_name, note_index):
    try:
        print(f"[INFO] check_sequence, checking note {note_index} in {song_name}, {songs[song_name][note_index]}")
        while True:
            arduino1.write(b'check note\n')
            line = arduino1.readline().decode('utf-8').strip()

            if not line:
                time.sleep(0.1)
                continue

            if line.startswith("Note"):
                note_info = line.split()  # Split the note info (e.g., "Note CU)")

                if len(note_info) < 2:
                    raise ValueError(f"check_sequence, malformed note message: '{line}'")

                note = note_info[1]  # Get the note (e.g., "C")
                print(note)
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
            leds.append(led_name_to_id[led_name])

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
                leds.append(led_name_to_id["down"])
            elif octave == '5':
                leds.append(led_name_to_id["up"]) #18 is led number
        
        # Send command if we have valid LED ids
        if leds:
            ids = ",".join(str(i) for i in leds)
            command = f"LED {ids} {color.upper()}\n"
            arduino1.write(command.encode('utf-8'))
            print(f"Sent: {command.strip()}")
        else:
            print("No valid LEDs determined from input.")

    except Exception as e:
        print(f"[ERROR] LED command failed for '{led_name}': {e}")



def detect_card():
    try:
        if arduino2.in_waiting > 0:
            line = arduino2.readline().decode('utf-8').strip()
            if line:
                print(f"UID from Arduino: {line}")
            song_name = card_to_song[line]
        
            print(f"[INFO] Card Detected: {song_name}")
            learning(song_name)

    except Exception as e:
        print(f"[ERROR] {e}")

def freestyle():
    global current_instrument, instrument_index
    led(current_instrument,"WHITE")
    try:
        arduino1.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino1.readline().decode('utf-8').strip()

        if not line:
            time.sleep(0.1)
            return
        
        elif line == "record_stop":
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
            arduino1.write(b'check note\n')  # Ask Arduino for pressed note
            recording_note_line = arduino1.readline().decode('utf-8').strip()

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

        arduino1.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino1.readline().decode('utf-8').strip()

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
                        led(songs[song_name][i],"GREEN")
                        play_note(songs[song_name][i])
                        result=check_sequence(song_name, i)
                        if not result:
                            success = False
                            led(songs[song_name][i],"off")
                            break
                    if success:
                        level = 2
                        print("[LEVEL 1] Complete! Moving to level 2.")
                        break
                    if not success:
                        print("[LEVEL 1] Wrong note, restarting level 1.")
                        file_path = os.path.join("wrong_sfx.mp3")
                        if os.path.exists(file_path):
                            pygame.mixer.Sound(file_path).play()
                            time.sleep(6)
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
                        led(songs[song_name][i],"Yellow")
                        play_note(songs[song_name][i])
                        led(songs[song_name][i],"off")
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
                        file_path = os.path.join("wrong_sfx.mp3")
                        if os.path.exists(file_path):
                            pygame.mixer.Sound(file_path).play()
                            time.sleep(6)
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
                for i in range(len(songs[song_name])):
                    play_note(songs[song_name][i])
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
                        file_path = os.path.join("wrong_sfx.mp3")
                        if os.path.exists(file_path):
                            pygame.mixer.Sound(file_path).play()
                            time.sleep(6)
                        level = 2
                        break

#main loop
led(current_instrument,)
try:
    while True:
        freestyle()
        detect_card()
except KeyboardInterrupt:
    print("Exiting...")
