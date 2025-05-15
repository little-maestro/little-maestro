import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

print("Reading from RFID Arduino...")

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print(f"UID from Arduino: {line}")
except KeyboardInterrupt:
    ser.close()
    print("Serial connection closed.")
