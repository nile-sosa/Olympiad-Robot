import serial
import time
import re

# Set the COM port and baud rate according to your Arduino setup
ser = serial.Serial('/dev/ttyACM1', 9600)  # Change 'COM3' to your actual port

try:
    while True:
        # Read a line from the serial port
        line = ser.readline()
        try:
            # Decode the line, ignoring or replacing invalid characters
            line = line.decode('utf-8').strip()
            matches = re.findall(r'enca(-?\d+)\tencb(-?\d+)', line)
            if matches:
                enca_value = int(matches[0][0])
                encb_value = int(matches[0][1])

                print("enca value:", enca_value)
                print("encb value:", encb_value)

        except UnicodeDecodeError as e:
            print("broken")
except KeyboardInterrupt:
    print("Serial communication stopped by the user.")

finally:
    # Close the serial port when done
    ser.close()

