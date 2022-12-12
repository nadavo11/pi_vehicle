from periphery import GPIO
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
        try:
            self.in1 = in1  # pin 1
            self.in2 = in2  # pin 2
        except(OSError):
            pass
        print(f'in1: {in1} , in2:{in2}\n')
        
        # init PWM pin 33
        self.pwm = PWM(pwm[0], pwm[1])

        # set PWM frequency
        self.pwm.frequency = 1e3

        # start PWM from 0
        self.pwm.duty_cycle = 0.01

        self.pwm.enable()
        self.in1.write(True)
        self.in2.write(False)

        print("\n motor was created!\n")
    def set_direction(self, direction):
        # write to GPIO
        print(direction)
        self.in1.write(direction[0])
        self.in2.write(direction[1])

    def set_vel(self, velocity):
        print(f'motor.set_vel called, v: {velocity}\n')
        self.pwm.duty_cycle = velocity
