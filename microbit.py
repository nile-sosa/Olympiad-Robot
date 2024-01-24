from microbit import *

uart.init(baudrate=115200)

right_motor = pin13
reverse_right = pin14
left_motor = pin15
reverse_left = pin16

while True:
    sleep(10)
    if uart.any():
        serial_input = uart.readline()
        if serial_input is not None:
            input2 = serial_input.decode('utf-8')# Decode the bytes to string
            left = input2[2:5]  # Use slicing instead of substr
            right = input2[5:8]  # Use slicing instead of substr
            print('recieved')
            print(input2)
            print(right)
            if len(input2) == 8 and input2[:1] == "mv":
                if left[0] == "-":
                    left_motor.write_analog(int(left[1:]))
                    reverse_left.write_digital(1)
                else:
                    left_motor.write_analog(int(left))
                    reverse_left.write_digital(0)  # Correct the pin to reverse_left
                if right[0] == "-":
                    right_motor.write_analog(int(right[1:]))
                    reverse_right.write_digital(1)  # Correct the pin to reverse_right
                else:
                    right_motor.write_analog(int(right))
                    reverse_right.write_digital(0)

