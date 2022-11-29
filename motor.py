from periphery import GPIO
import keyboard
from periphery import PWM
import time


class Motor:
    def __init__(self, in1, in2, pwm):
        """

        :param in1: tuple, (_path,_pin number)
        :param in2: tuple, (_path,_pin number)
        :param pwm: tuple, (_chip#,_channel)

        """
        # ------ in1,2 Settings-----
        self.in1 = GPIO(in1[0], in1[1], "out")  # pin 1
        self.in2 = GPIO(in2[0], in2[1], "out")  # pin 2

        # init PWM pin 33
        self.pwm = PWM(pwm[0], pwm[1])

        # set PWM frequency
        self.pwm.frequency = 1e3

        # start PWM from 0
        self.pwm.duty_cycle = 0

        self.pwm.enable()

    def set_direction(self, direction):
        # write to GPIO
        self.in1.write(direction[0])
        self.in2.write(direction[1])

    def set_vel(self, velocity):
        self.pwm.duty_cycle = velocity
