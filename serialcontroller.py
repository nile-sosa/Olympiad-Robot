import serial
import threading as th
import time
from multiprocessing import Process, Value, Manager


gyro_process = None
current_thread = None
stop_event = th.Event()
manager = Manager()
absolute_z = manager.Value('d', 0.0)


def straight(speed):

    microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0)
    base_speed = speed
    try:
        while not stop_event.is_set():
            speed_left = int(speed)
            speed_right = int(speed)
            enc1_val = 0
            enc2_val = 0
            ##print(speed_left)
            if (speed_left==0) and (speed_right==0):
                print("stopped")
                motor_speeds = f"mv000000\n"
            elif enc1_val < enc2_val:
                speed_left = int(speed) + 20
                motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
                print("left behind")
            elif enc2_val < enc1_val:
                speed_right = int(speed) + 30
                motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
                print("right behind")
            else:
                motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print(motor_speeds)
            print(str(enc1_val)+","+str(enc2_val))
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
