import serial
import threading as th

previous_run = 0
clean = 0
current_thread = None
stop_event = th.Event()


def straight(speed):
    global clean
    compass_vals = []

    microbit = serial.Serial("COM5",115200,timeout = 0.1)
    x = 0

    ##Gets four compass readings and avergaes for accurate initial
    ##direction
    
    
    while x < 5:
        microbit.write(b"mv000000\n")
        data = microbit.readline().decode('utf-8').rstrip()
        if len(data)==3:
            clean = data
            compass_vals.append(int(clean))
        x=x+1
        
    init_direction = sum(compass_vals)/len(compass_vals)

    speed_left = speed
    speed_right = speed
    base_speed = speed
    
    try:
        while not stop_event.is_set():
            motor_speeds = f"mv{speed_left}{speed_right}\n" 
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            if len(data)==3:
                clean = data
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
