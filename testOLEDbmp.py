import serial
import time
arduino2 = None

if serial:
    try: 
        arduino2 = serial.Serial('/dev/serial/by-path/platform-70090000.xusb-usb-0:2.3:1.0-port0', 9600, timeout=1) # Card Reader
        time.sleep(2)  # Give Arduino time to reset
        print("Connected to Arduino.")
    except serial.SerialException:
        print("Not connected to an Arduino.")

commandList = ["jump","level1","level2","level3","win","wrong","HBD","JB","canon"]

for message in commandList:
    arduino2.write((message+"\n").encode('utf-8'))
    print(f"sent {message}")
    time.sleep(4)


