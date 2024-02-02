from serialcontroller import motor_controller as mc
import time
import sys
import serial

microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.001)

while False:
    data = microbit.readline().decode('utf-8').rstrip()
    if data == "start":
        break
    print(data)

if __name__ == "__main__":
    mc(None,"reverse",-200)

