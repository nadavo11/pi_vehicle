
import sys
import termios
import tty
import Vehicle
import wheel
from motor import Motor
from Vehicle import Vehicle

from periphery import GPIO



if __name__ == "__main__":

    
    in1 = ["/dev/gpiochip2", 9] #pin 16
    in2 = ["/dev/gpiochip4", 10]    #pin 18
    pwmA = [1,0]    # pin 33

    in3 = ["/dev/gpiochip4", 13]
    in4 = ["/dev/gpiochip2", 13]
    pwmB = [0,0] #pin 32
    
    in1 = GPIO(in1[0],in1[1],"out")
    in2 = GPIO(in2[0],in2[1],"out")


    in3 = GPIO(in3[0],in3[1],"out")
    in4 = GPIO(in4[0],in4[1],"out")
    
    print(f'vech in1:{in1}')
    right_motor = Motor(in1, in2, pwmA)
    print('\nright motor done!\n')
    left_motor = Motor(in3, in4, pwmB)


    vehicle = Vehicle(left_motor,right_motor)

    print(vehicle)


    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, filedescriptors)









