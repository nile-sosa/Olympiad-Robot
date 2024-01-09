import serial
import threading as th
from gyro import gyro_reader
import time
from multiprocessing import Process, Value, Manager

gyro_process = None
current_thread = None
stop_event = th.Event()

manager = Manager()
absolute_z = manager.Value('d', 0.0)

def straight(speed):

    microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0.1)


    speed_left = speed
    speed_right = speed
    base_speed = speed
    
    try:
        while not stop_event.is_set():
            motor_speeds = f"mv{speed_left}{speed_right}\n" 
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print(data)
            print(absolute_z.value)
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
    
    gyro_process = Process(target = gyro_reader, args=(absolute_z,))
    gyro_process.start()
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
