from microbit import *

uart.init(baudrate=115200)

right_motor = pin15
reverse_right = pin16
left_motor = pin13
reverse_left = pin14

while True:
    sleep(20)
    if uart.any():
        serial_input = uart.readline()
        if serial_input is not None:
            input2 = serial_input.decode('utf-8')# Decode the bytes to string
            input2 = input2.strip()
            left = input2[2:5]  # Use slicing instead of substr
            right = input2[5:8]  # Use slicing instead of substr
            print(left)
            print(right)
    
            if len(input2) == 8 and input2[:2] == "mv":
                if left[0] == "-":
                    print("reverse")
                    left_motor.write_analog(abs(int(left))*10)
                    reverse_left.write_digital(0)  # Correct the pin to reverse_left
                else:
                    print("forward")
                    left_motor.write_analog((100-int(left[1:]))*10)
                    reverse_left.write_digital(1)
                if right[0] == "-":
                    right_motor.write_analog(abs(int(right))*10)
                    reverse_right.write_digital(0)
                else:
                    right_motor.write_analog((100-int(right[1:]))*10)
                    reverse_right.write_digital(1)  # Correct the pin to reverse_right

