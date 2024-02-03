import serial
import time
microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.001)


while True:
    print("dasfdsafseafsefadaef")
    x=10
    clean = 0
    while x<90:
        time.sleep(0.05)
        writer =   f"mv0{x}0{x}\n"
        microbit.write(writer.encode("utf-8"))
        data = microbit.readline().decode('utf-8').rstrip()

        print(data)
        x+=1

    x=0
    clean = 0
    while x<20:
        time.sleep(0.1)
        microbit.write(b'mv-00-00\n')
        data = microbit.readline().decode('utf-8').rstrip()

        print(data)
        x+=1

microbit.close() 
