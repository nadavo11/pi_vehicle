from periphery import GPIO
import keyboard
from periphery import PWM
import time

MINVEL, MAXVEL = -1, 1


class Wheel:

    def __init__(self):
        self.vel = 0

    def set_vel(self, v):
        # invalid value protection
        if MAXVEL > v or v < MINVEL:
            return 0

        self.vel = v
        return 1

    # override < += > operator
    def __iadd__(self, other):
        return self.set_vel(self.vel + other)

    # override < -= > operator
    def __isub__(self, other):
        return self.set_vel(self.vel - other)

    def stop(self):
        self.set_vel(0)

