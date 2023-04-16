import periphery

from periphery import GPIO
from periphery import PWM

import signal
import time
import os

from motor import Motor
from wheel import Wheel
from Vehicle import Vehicle
from detect import detect


# TODO: SHUTDOWN function


def vehicle_init():
    """
    *********************************************************

                Vehicle initialization

    *********************************************************
    """

    in1 = ["/dev/gpiochip2", 9]  # pin 16
    in2 = ["/dev/gpiochip4", 10]  # pin 18
    pwmA = [0, 0]  # pin 32

    in3 = ["/dev/gpiochip4", 13]
    in4 = ["/dev/gpiochip2", 13]
    pwmB = [1, 0]  # pin 33

    # Open GPIO /dev/gpiochip0 line 10 with input direction
    in1 = GPIO(in1[0], in1[1], "out")
    in2 = GPIO(in2[0], in2[1], "out")

    in3 = GPIO(in3[0], in3[1], "out")
    in4 = GPIO(in4[0], in4[1], "out")

    print(f'vech in1:{in1}')
    right_motor = Motor(in1, in2, pwmA)
    print('\nright motor done!\n')
    left_motor = Motor(in3, in4, pwmB)

    vehicle = Vehicle(left_motor, right_motor)
    print(vehicle)
    return vehicle


def follow_obj(objs, vehicle):
    ### detect people
    people = [obj for obj in objs if obj.id == 43]
    p_location = 0
    p_size = 0

    ### get location of the first person
    if people:

        p = people[0]

        p_location = (p.bbox.xmin + p.bbox.xmax - 300) / 2
        p_size = p.bbox.ymax - p.bbox.ymin
        print(f'person at : {p_location}')

        if p_location > 60:
            vehicle.turn(0.9)

        elif p_location < -60:
            vehicle.turn(-0.9)

        else:
            if p_size < 100:
                vehicle.set_vel(-0.9)

            elif p_size > 150:
                vehicle.set_vel(0.9)
            else:
                vehicle.stop()

    else:
        vehicle.stop()


"""----------------------------------
            Main
------------------------------------"""
vehicle = vehicle_init()
"""----------------------------------
define a safe-shutdown signal handler
------------------------------------"""


def sig_handler(SIG, FRAME):
    vehicle.shutdown()
    os.kill(os.getpid(), signal.SIGINT)


signal.signal(signal.SIGINT, sig_handler)

"""----------------------------------
detection and driving the vehicle
------------------------------------"""
detect(vehicle, follow_obj)
