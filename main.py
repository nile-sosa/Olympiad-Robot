from serialcontroller import motor_controller as mc
import time
import sys
import serial

microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.001)

while True:
    data = microbit.readline().decode('utf-8').rstrip()
    print(data)
    if data == "start":
        time.sleep(2.5)
        break
    print(data)

if __name__ == "__main__":
    mc(None,"forward",348)
    mc(None,"forward",810)
    mc(None,"left",0)
    mc(None,"forward",1215)
    mc(None,"left",0)
    mc(None,"forward",810)
    mc(None,"left",0)
    mc(None,"left",0)
    mc(None,"forward",1215)
    mc(None,"right",0)
    mc(None,"forward",405)
