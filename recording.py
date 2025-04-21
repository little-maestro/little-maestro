def freestyle():
    global mode
    recorded_song = []
    print("[MODE] Freestyle Mode")
    while True:



        if card_line == "CARD_DETECTED":  
            return detect_card()  # Switch mode if a card is detected
         
        arduino.write(b'check note\n')  # Ask Arduino for pressed note
        line = arduino.readline().decode('utf-8').strip()
        
        if line == "Record":
            record = True
            while record:
                arduino.write(b'check note\n')  # Ask Arduino for pressed note
                note_line = arduino.readline().decode('utf-8').strip()

                if note_line.startswith("Note"):
                    note = line.split()[1]
                    recorded_song.append(note)
                
                elif note_line == ("Record_Stop"):
                    return
                else:
                    print(f"[INFO] Unrecognized serial message: '{note_line}'")
        
        elif line.startswith("Note"):
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