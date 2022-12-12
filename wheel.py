from periphery import GPIO
import keyboard
from periphery import PWM
import time
from motor import Motor

MINVEL, MAXVEL = -1, 1
directions = {"forward": (True, False), "backward": (False, True), "disable": (False, False)}


class Wheel:
    def __init__(self,motor):
        """

        :param motor:
        """
        self.vel = 0

        self.direction = "disable"
        self.motor = motor



    def set_direction(self,d):
        if self.direction == d:
            return 1

        # set motor spin direction
        self.motor.set_direction(directions[d])

        self.direction = d
        return 0

    def set_vel(self, v):
        print('w.setvel called')

        # invalid value protection
        if MAXVEL <= v or v <= MINVEL:
            return 0
        # moving forward or backward
        if v > 0:
            self.set_direction("forward")
        if v < 0:
            self.set_direction("backward")
        if v == 0:
            self.set_direction("disable")

        self.vel = v
        self.motor.set_vel(abs(v))
        return 1

    # override < += > operator
    def __iadd__(self, other):
        self.set_vel(self.vel + other)

    # override < -= > operator
    def __isub__(self, other):
        self.set_vel(self.vel - other)

    def stop(self):
        self.set_vel(0)

