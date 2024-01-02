import serial
import threading as th


current_thread = None
stop_event = th.Event()


def straight(speed):

    microbit = serial.Serial("COM5",115200,timeout = 0.1)


    speed_left = speed
    speed_right = speed
    base_speed = speed
    
    try:
        while not stop_event.is_set():
            motor_speeds = f"mv{speed_left}{speed_right}\n" 
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print(data)
    except KeyboardInterrupt as a:
        pass

    microbit.close()

def left():
    pass

def right():
    pass

def motor_controller(speed,direction):
    global current_thread
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
