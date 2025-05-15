#testing the buttons connect from arduino to jetson

import serial
import time

from serial import Serial
serial_port = "/dev/ttyUSB0"
baud_rate = 9600

# Open serial connection
arduino = serial.Serial(serial_port, baud_rate, timeout=1)
time.sleep(2)  # Wait for Arduino to reset

try:
    while True:
        arduino.write(b"check note\n")  # Send command
        time.sleep(0.1)
        
        # Read lines sent from Arduino
        while arduino.in_waiting:
            line = arduino.readline().decode("utf-8").strip()
            if line:
                print("Arduino says: {line}")

        time.sleep(0.5)  # Avoid flooding serial
except KeyboardInterrupt:
    arduino.close()
    print("Serial connection closed.")
