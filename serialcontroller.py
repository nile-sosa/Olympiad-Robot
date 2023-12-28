import serial
import time
import multiprocessing as mp
import os
import signal


previous_run = 0
clean = 0
current = "none"

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
    
    while True:
        motor_speeds = f"mv{speed_left}{speed_right}\n" 
        microbit.write(motor_speeds.encode("utf-8"))
        data = microbit.readline().decode('utf-8').rstrip()
        if len(data)==3:
            clean = data

def left():
    pass

def right():
    pass

def motor_controller(speed,direction):
    global current
    if current != "none":
        os.kill(current, signal.SIGTERM)
    if direction == "straight":
        motorp = mp.Process(target = straight, args=(speed,))
    elif direction == "right":
        motorp = mp.Process(target = right, args=(speed,))
    elif direction == "left":
        motorp = mp.Process(target = left, args=(speed,))
    motorp.start()
    current = motorp.pid
    print(current)

