from serialcontroller import motor_controller
import time
import sys

##Use a string for motor values, not an int

##since daemon threading is used, time wait must be used to keep motor program running
if __name__ == "__main__":
    motor_controller("050","straight")
    time.sleep(6)
    motor_controller("000","straight")
    time.sleep(2)
    sys.exit()
