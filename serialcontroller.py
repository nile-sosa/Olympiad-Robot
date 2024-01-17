import serial
import threading as th
import time
from multiprocessing import Process, Value, Manager
import Encoder

enc1 = Encoder.Encoder(17,27)
enc2 = Encoder.Encoder(23,24)
gyro_process = None
current_thread = None
stop_event = th.Event()
manager = Manager()
absolute_z = manager.Value('d', 0.0)


def straight(speed):

    microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.1)


    speed_left = int(speed)
    speed_right = int(speed)
    base_speed = speed
    
    try:
        while not stop_event.is_set():
            enc1_val = enc1.read()
            enc2_val = enc2.read()
            print(speed_left)
            if ((speed_left==0) or (speed_left=="00")) and ((speed_right==0) or (speed_right=="00")):
                print("stopped")
                speed_left = "00"
                speed_right = "00"
            elif enc1_val > enc2_val:
                speed_left = int(speed) + 10
            elif enc2_val > enc1_val:
                speed_right = int(speed) + 10
            motor_speeds = f"mv0{speed_left}0{speed_right}\n" 
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            ##print(motor_speeds)
            ##print(str(enc1_val)+","+str(enc2_val))
    except KeyboardInterrupt as a:
        microbit.close()
        pass

    microbit.close()
    

def left():
    pass

def right():
    pass

def motor_controller(speed,direction):
    global bearing
    global current_thread
    global gyro_process
    
    ##gyro_process = Process(target = gyro_reader, args=(absolute_z,))
    ##gyro_process.start()
    if current_thread and current_thread.is_alive():
        stop_event.set()
        current_thread.join()

    stop_event.clear()

    if direction == "straight":
        motorp = th.Thread(target = straight, args=(speed,))
        current_thread = motorp

##Setting daemon to true allows thread to end when main process finishes
    current_thread.daemon = True
    current_thread.start()
