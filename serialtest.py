import serial
import Encoder
enc1 = Encoder.Encoder(17,27)
enc2 = Encoder.Encoder(23,24)
microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.001)
x=0
clean = 0
while x<650:
    microbit.write(b'mv050050\n')
    data = microbit.readline().decode('utf-8').rstrip()
    if len(data)==3:
        clean = data

    print(clean)
    print(str(enc1.read())+","+str(enc2.read()))
    x+=1

x=0
clean = 0
while x<1000:
    microbit.write(b'mv000000\n')
    data = microbit.readline().decode('utf-8').rstrip()
    if len(data)==3:
        clean = data

    print(clean)
    print(str(enc1.read()) + "," + str(enc2.read()))
    x+=1

microbit.close() 
