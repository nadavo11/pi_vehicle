
import sys
import termios
import tty
import Vehicle
import wheel
import motor
import Vehicle
from main import gpio_in

in1 = ["/dev/gpiochip2", 9] #pin 16
in2 = ["/dev/gpiochip4", 10]    #pin 18
pwmA = [1,0]    # pin 33

in3 = ["/dev/gpiochip4", 13]
in4 = ["/dev/gpiochip2", 13]
pwmB = [0,0] #pin 32

right_motor = motor.Motor(in1, in2, pwmA)
left_motor = motor.Motor(in3, in4, pwmB)

vehicle = Vehicle.Vehicle(left_motor,right_motor)

filedescriptors = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin)
x = 0

try:
    while 1:
        x = sys.stdin.read(1)[0]

        # forward
        if x == "w":
            vehicle.forward_step()
        if x == "j":
            vehicle += 1

        if x == "k":
            vehicle -= 1
        # left
        if x == "a":
            vehicle.turn_left()
        # right
        if x == "d":
            vehicle.turn_right()

        # back
        if x == "s":
            vehicle.backward_step()
        if x == "p":
            break


finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)
