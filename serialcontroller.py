import serial
import time
import multiprocessing as mp


microbit = serial.Serial("COM5",115200,timeout = 0.001)
x=0
clean = 0
while x<100:
    microbit.write(b'4040\n')
    data = microbit.readline().decode('utf-8').rstrip()
    if len(data)==3:
        clean = data

    print(clean)
    x+=1


microbit.close() 
 