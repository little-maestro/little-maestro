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

# Function to switch to Learning Mode
def switch_to_learning():
    global mode
    mode = "learning"
    learning()

# Function to switch back to Freestyle Mode
def switch_to_freestyle():
    global mode
    mode = "freestyle"
    freestyle()