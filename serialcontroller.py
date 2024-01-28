import serial
import threading as th
import time
from multiprocessing import Process, Value, Manager
from encoder import encoder 

process_called = False
encoder_process = None
incrementor_thread = None
current_thread = None
stop_event = th.Event()
manager = Manager()
encoder_values = manager.list([0,0])
incrementor_list = [0]

def straight(speed):
    global encoder_values
    global encoder_process

    microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0)
    base_speed = speed
    try:
        while not stop_event.is_set():
            time.sleep(0.05)
            print(encoder_process.is_alive())
            speed_left = int(speed)
            speed_right = int(speed)
            enc1_val = encoder_values[0]
            enc2_val = encoder_values[1]
            ##print(speed_left)
            if (speed_left==0) and (speed_right==0):
                print("stopped")
                motor_speeds = f"mv-00-00\n"
            elif enc1_val < enc2_val:
                speed_left = int(speed) + 5
                motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
                print("left behind")
            elif enc2_val < enc1_val:
                speed_right = int(speed) + 5
                motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
                print("right behind")
            else:
                motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            #print("enc1:" + str(enc1_val))
            #print("enc2:" + str(enc2_val))
            #print(encoder_values)
            #print(motor_speeds)
            print(incrementor_list)
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
    global process_called
    global current_thread
    global encoder_process
    global incrementor_thread
    global incrementor_list
    if not process_called:
        encoder_process = Process(target = encoder, args=(encoder_values,))
        process_called = True
    if not encoder_process.is_alive():
        encoder_process.start()
        time.sleep(2)
    if current_thread and current_thread.is_alive():
        stop_event.set()
        current_thread.join()

    stop_event.clear()

    if direction == "straight":
        motorp = th.Thread(target = straight, args=(speed,))
        current_thread = motorp
    incrementor_list[0] = 0
    incrementor_thread = th.Thread(target = incrementor, args=(incrementor_list,))
    incrementor_thread.daemon = True
    incrementor_thread.start()
    current_thread.daemon = True
    current_thread.start()

def incrementor(incrementation_value):
    while not stop_event.is_set():
        time.sleep(0.015)
        incrementation_value[0] = incrementation_value[0] + 1
    print("incrementation stopped")
##Setting daemon to true allows thread to end when main process finishes
