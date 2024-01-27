import serial
import time
import re

# Set the COM port and baud rate according to your Arduino setup
ser = serial.Serial('/dev/ttyACM1', 9600)  # Change 'COM3' to your actual port

def encoder(encoder_list):
    global broke_down
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


                encoder_list[0] = enca_value
                encoder_list[1] = encb_value
                if __name__ == "__main__":
                    print(encoder_list)
        except UnicodeDecodeError as e:
            print("broken")

if __name__ == "__main__":
    list =[0,0]
    encoder(list)


