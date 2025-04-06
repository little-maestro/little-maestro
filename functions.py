import serial
import time

from little_maestro_sound import play_note_instrument


# Serial communication setup (change the port if needed)
arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)  # Give Arduino time to reset

def check_sequence(song_name, note_sequence):
    while True:
        arduino.write(b'check note\n')
        line = arduino.readline().decode('utf-8').strip()
        if line:
            if line.startswith("Note"):
                note_info = line.split()  # Split the note info (e.g., "Note CU)")
                note = note_info[1]  # Get the note (e.g., "C")
                # Play the corresponding note sound
                play_note_instrument(note, instrument)

                # Check if the received note matches the expected note
                if note == songs[song_name][note_sequence]:
                    print('Corect')
                    return
                elif line != songs[song_name][note_sequence]:
                    print('Incorrect')
                    return

def led(led_ids, color):
    if isinstance(led_ids, list):
        ids = ",".join(str(i) for i in led_ids)
    else:
        ids = str(led_ids)
    command = f"LED {ids} {color.upper()}\n"
    arduino.write(command.encode('utf-8'))
    print(f"Sent: {command.strip()}")


