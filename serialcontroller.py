import serial
import time
import threading as th

previous_run = 0
clean = 0
current_thread = None
stop_event = th.Event()  # Event to signal the thread to stop

def straight(speed):
    global clean
    compass_vals = []

    microbit = serial.Serial("COM5", 115200, timeout=0.1)
    x = 0

    # Gets four compass readings and averages for accurate initial direction
    while x < 5:
        microbit.write(b"mv000000\n")
        data = microbit.readline().decode('utf-8').rstrip()
        if len(data) == 3:
            clean = data
            compass_vals.append(int(clean))
        x = x + 1

    init_direction = sum(compass_vals) / len(compass_vals)

    speed_left = speed
    speed_right = speed
    base_speed = speed

    while not stop_event.is_set():
        motor_speeds = f"mv{speed_left}{speed_right}\n"
        microbit.write(motor_speeds.encode("utf-8"))
        data = microbit.readline().decode('utf-8').rstrip()
        if len(data) == 3:
            clean = data

    # Ensure that the microbit serial connection is properly closed
    microbit.close()

def left():
    pass

def right():
    pass

class MotorThread(th.Thread):
    def __init__(self, speed, direction):
        super().__init__()
        self.speed = speed
        self.direction = direction

    def run(self):
        global current_thread
        if current_thread and current_thread.is_alive():
            stop_event.set()  # Signal the current thread to stop
            current_thread.join()

        stop_event.clear()  # Reset the stop event for the new thread

        if self.direction == "straight":
            current_thread = self
            self.straight()
        elif self.direction == "right":
            current_thread = self
            self.right()
        elif self.direction == "left":
            current_thread = self
            self.left()

    def straight(self):
        straight(self.speed)

    def left(self):
        left()

    def right(self):
        right()

# Usage:
# Call motor_controller to start/stop the motor movement
# Example: motor_controller(50, "straight")
# Example: motor_controller(30, "left")
# Example: motor_controller(40, "right")
def motor_controller(speed, direction):
    global current_thread
    if current_thread and current_thread.is_alive():
        stop_event.set()  # Signal the current thread to stop
        current_thread.join()

    stop_event.clear()  # Reset the stop event for the new thread

    motor_thread = MotorThread(speed, direction)
    motor_thread.start()
    current_thread = motor_thread
