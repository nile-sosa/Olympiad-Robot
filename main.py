from serialcontroller import motor_controller
import multiprocessing as mp
import serialcontroller
import time

##Use a string for motor values, not an int

##since daemon threading is used, time wait must be used to keep motor program running
if __name__ == "__main__":
    while True:
        motor_controller("000","straight")
        time.sleep(2)
    
