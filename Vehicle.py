
from periphery import GPIO
import keyboard
from periphery import PWM
import time

from wheel import Wheel

MINVEL, MAXVEL = -1, 1

class Vehicle:
    def __init__(self, motor_left,motor_right):

        #initiate 2 wheels
        self.left_wheel = Wheel(motor_left)
        self.right_wheel = Wheel(motor_right)

        print(self.left_wheel)
        self.vel = 0
        self.angle = 0
        self.acc = 0

    def set_vel(self, v):

        print('v.setvel called')
        if not (MINVEL <= v <= MAXVEL):
            return 0
        self.left_wheel.set_vel(v)
        self.right_wheel.set_vel(v)
        
        self.vel = v
        print(f'v:{v}')
        return 1

    def stop(self):
        self.set_vel(0)
        

    def turn(self, turn):
        self.left_wheel.set_vel(self.vel + turn)
        self.right_wheel.set_vel(self.vel - turn)

    def step(self, v,t):
        self.set_vel(v)
        time.sleep(t)
        self.stop()
    def forward_step(self):
        self.step(0.3,0.3)

    def backward_step(self):
        self.step(-0.3,0.3)

    def turn_left(self):
        self.turn(-0.3)
        time.sleep(0.3)
        self.stop()

    def turn_right(self):
        self.turn(0.3)
        time.sleep(0.3)
        self.stop()
    def shutdown(self):
        self.left_wheel.shutdown()
        self.right_wheel.shutdown()

    def __iadd__(self, other):
        self.left_wheel += 1
        self.right_wheel += 1

    def __isub__(self, other):
        self.left_wheel -= 1
        self.right_wheel -= 1
