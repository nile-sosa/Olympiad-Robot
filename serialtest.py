import serial


microbit = serial.Serial("COM5",115200,timeout = 0.001)
x=0
clean = 0
while x<1000:
    microbit.write(b'mv000000\n')
    data = microbit.readline().decode('utf-8').rstrip()
    if len(data)==3:
        clean = data

    print(clean)
    x+=1

microbit.close() 