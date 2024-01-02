right = ""
left = ""
input2 = ""
serial.set_baud_rate(BaudRate.BAUD_RATE115200)

def on_forever():
    global input2, left, right
    input2 = serial.read_line()
    left = input2.substr(2, 3)
    right = input2.substr(5, 3)
    if len(input2) == 8 and input2.substr(0, 2) == "mv":
        if left.substr(0, 1) == "-":
            motion.drive_wheel(Motor.LEFT, -100 - parse_float(left))
        else:
            motion.drive_wheel(Motor.LEFT, parse_float(left))
        if right.substr(0, 1) == "-":
            motion.drive_wheel(Motor.RIGHT, -100 - parse_float(right))
        else:
            motion.drive_wheel(Motor.RIGHT, parse_float(right))
    serial.write_line(input2)
basic.forever(on_forever)
