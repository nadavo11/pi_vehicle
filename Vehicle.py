
from periphery import GPIO
import keyboard
from periphery import PWM
import time

from wheel import Wheel

MINVEL, MAXVEL = -1, 1

class Vehicle:
    def __init__(self, motor_left,motor_right) -> None:

        #initiate 2 wheels
        self.left_wheel = Wheel(motor_left)
        self.right_wheel = Wheel(motor_right)


        self.vel = 0
        self.turn = 0
        self.acc = 0

    def set_vel(self, v):
        if not (MINVEL <= v <= MAXVEL):
            return 0
        self.left_wheel.set_vel(v)
        self.right_wheel.set_vel(v)
        return 1

    def stop(self):
        self.left_wheel.set_vel(0)
        self.right_wheel.set_vel(0)

    def turn(self, turn):
        self.left_wheel += turn
        self.right_wheel -= turn

