from serialcontroller import motor_controller
import multiprocessing as mp
import serialcontroller
import time

##Use a string for motor values, not an int

if __name__ == "__main__":
    while True:
        motor_controller("-20","straight")
        time.sleep(3)
        motor_controller("020","straight")
        time.sleep(3)
