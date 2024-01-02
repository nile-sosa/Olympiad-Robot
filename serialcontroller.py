import serial
import threading as th
from gyro import gyro_reader

gyro_thread = None
current_thread = None
stop_event = th.Event()
bearing = [0]


def straight(speed):
    global bearing

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
            print(bearing)
    except KeyboardInterrupt as a:
        pass

    microbit.close()

def left():
    pass

def right():
    pass

def motor_controller(speed,direction):
    global bearing
    global current_thread
    global gyro_thread
    
    gyro_thread = th.Thread(target = gyro_reader, args=(bearing,))
    gyro_thread.start()
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
