from serialcontroller import motor_controller as mc
import time
import sys
import serial

microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.001)

while True:
    data = microbit.readline().decode('utf-8').rstrip()
    print(data)
    if data == "start":
        break
    time.sleep(2.5)
    print(data)

if __name__ == "__main__":
    mc(None,"forward",350)
    mc(None,"left",0)
    mc(None,"forward",400)
    mc(None,"right",0)
    mc(None,"forward",400)
    mc(None,"right",0)
    mc(None,"forward",400)
    mc(None,"left",0)
    mc(None,"forward",400)
    mc(None,"reverse",-400)

