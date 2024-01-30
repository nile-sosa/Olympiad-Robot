import serial
import threading as th
import time

from multiprocessing import Process, Value, Manager
from encoder import encoder 
from simple_pid import PID

process_called = False
encoder_process = None
incrementor_thread = None
current_thread = None
stop_event = th.Event()
manager = Manager()
encoder_values = manager.list([0,0])
incrementor_list = [0]

kp = 4.0
ki = 1
kd = 1.3

left_pid_motor = PID(kp,ki,kd,setpoint = 0)
right_pid_motor = PID(kp,ki,kd,setpoint = 0)

def straight(distance):
    global encoder_values
    init_left = encoder_values[0]
    init_right = encoder_values[1]
    left_pid_motor.output_limits=(-900,900)
    right_pid_motor.output_limits=(-900,900)
    print("starting motors forward")
    i = 0
    microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0)
    try:
        while encoder_values[0]-init_left <= distance:
            time.sleep(0.05)
            left_pid_motor.setpoint = incrementor_list[0]
            right_pid_motor.setpoint = incrementor_list[0]
            left_enc_val = encoder_values[0] - init_left
            right_enc_val = encoder_values[1] - init_right

            left_pid_output = left_pid_motor(left_enc_val)/10
            right_pid_output = right_pid_motor(right_enc_val)/10
            print(left_pid_output)
            print(right_pid_output)
            speed_left = int(left_pid_output)
            speed_right = int(right_pid_output)

            motor_speeds = f"mv0{speed_left}0{speed_right}\n"   
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print([left_enc_val,right_enc_val])
            #print(motor_speeds)
            print(incrementor_list)
        while i<10:
            motor_speeds = f"mv-00-00\n"   
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print("stopping")
            i=i+1
    except KeyboardInterrupt as a:
        microbit.close()
        pass

    microbit.close()

def left():
    global encoder_values
    init_left = encoder_values[0]
    init_right = encoder_values[1]
    print("turning left")
    i=0
    turn = 143
    right_pid_motor.setpoint = -turn
    right_pid_motor.output_limits = (-650,650)
    left_pid_motor.setpoint = turn
    left_pid_motor.output_limits = (-650,650)
    microbit = serial.Serial("/dev/ttyACM0",115200,timeout = 0)
    try:
        while encoder_values[1]-init_right>=-turn or encoder_values[0]-init_left<=turn:
            time.sleep(0.05)
            left_enc_val = encoder_values[0] - init_left
            right_enc_val = encoder_values[1] - init_right

            left_pid_output = left_pid_motor(left_enc_val)/10
            right_pid_output = right_pid_motor(right_enc_val)/10
            print(left_pid_output)
            print(right_pid_output)
            speed_left = int(left_pid_output)
            speed_right = int(right_pid_output)
            if encoder_values[1]-init_right<=-turn:
                speed_right = "000"
            if encoder_values[0]-init_left>=turn:
                speed_left = "00"
            motor_speeds = f"mv0{speed_left}{speed_right}\n"   
            print(motor_speeds)
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print([left_enc_val,right_enc_val])
        while i<10:
            motor_speeds = f"mv-00-00\n"   
            microbit.write(motor_speeds.encode("utf-8"))
            data = microbit.readline().decode('utf-8').rstrip()
            print("stopping")
            i=i+1
    except KeyboardInterrupt as a:
        microbit.close()
        pass


def right():
    pass

def motor_controller(speed,direction,distance):
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
        motorp = th.Thread(target = straight, args=(distance,))
        current_thread = motorp
    elif direction == "left":
        motorp = th.Thread(target = left, args=())
        current_thread = motorp
    incrementor_list[0] = 0
    incrementor_thread = th.Thread(target = incrementor, args=(incrementor_list,distance))
    incrementor_thread.daemon = True
    incrementor_thread.start()
    current_thread.start()

def incrementor(incrementation_value,distance):
    while incrementation_value[0]<distance:
        time.sleep(0.01)
        incrementation_value[0] = incrementation_value[0] + 1
    print("incrementation stopped")
##Setting daemon to true allows thread to end when main process finishes
