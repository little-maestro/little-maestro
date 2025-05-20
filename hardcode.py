import time
import pygame
pygame.mixer.init()
import os
os.chdir(".")
import serial

tempo = 0.5
ser = serial.Serial('/dev/serial/by-path/platform-70090000.xusb-usb-0:2.1.4:1.0-port0', 9600, timeout=1) # Card Reader
surat = None


def play_note(note):
    file_name = f"{note}.mp3"
    instrument_folder = "piano" + "_directory"
    file_path = os.path.join(instrument_folder, file_name)
    print(file_path)
        
    if os.path.exists(file_path):
        pygame.mixer.Sound(file_path).play()
        print(f"[INFO] Playing: piano - {note}")
        time.sleep(tempo)  # Adjust delay based on tempo

    else:
        raise ValueError(f"play_note, Error: {file_path} not found!")

songs =["G3", "G3", "A3","G3", "C4", "B3", "G3", "G3", "A3", "G3", "D4", "C4",
                "G3", "G3", "G4", "E4", "C4", "B3", "A3", "F4", "F4", "E4", "C4", "D4", "C4"]
print("Reading from RFID Arduino...")

try:
    while True:
        print(f"reading buffer: {ser.in_waiting}")
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"UID from Arduino: {line}")
                if len(line) == 8 and surat != "jetson":
                    for i in songs:
                        play_note(i)
                    surat = "jetson"
                else:
                    surat = "end"
                    ser.flushInput()
                    ser.flushOutput()
                    print("ending")
        print(surat)
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
