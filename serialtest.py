import serial
import time
microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.001)
 
while True:
    x=0
    clean = 0
    while x<250:
        microbit.write(b'mv030030\n')
        data = microbit.readline().decode('utf-8').rstrip()

        print(data)
        x+=1

    x=0
    clean = 0
    while x<1000:
        microbit.write(b'mv000000\n')
        data = microbit.readline().decode('utf-8').rstrip()

        print(data)
        x+=1

microbit.close() 
