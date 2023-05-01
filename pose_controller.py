
import argparse

import numpy as np
from PIL import Image
from PIL import ImageDraw
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
import numpy as np
import signal
import sys
import time
import os
from motor import Motor
from wheel import Wheel
from Vehicle import Vehicle
from detect import detect
import argparse

from periphery import GPIO,PWM
_NUM_KEYPOINTS = 17
LEFT = 1
RIGHT = 0
hand_raised = [0,0]


def det_pose(input):
    parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
      '-m', '--model', required=True, help='File path of .tflite file.')
    args = parser.parse_args()



    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()
    img = Image.fromarray(inp)
    resized_img = img.resize(common.input_size(interpreter), Image.ANTIALIAS)
    common.set_input(interpreter, resized_img)

    interpreter.invoke()

    pose = common.output_tensor(interpreter, 0).copy().reshape(_NUM_KEYPOINTS, 3)


#    print(pose)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    hands = pose[9:11]
    sholders = pose[5:7]

    hand_raised[RIGHT] = hands[RIGHT, 0] < sholders[RIGHT, 0]
    hand_raised[LEFT] = hands[LEFT, 0] < sholders[LEFT, 0]
    for i, hand in enumerate(hands):
        draw.ellipse(
            xy=[
                hand[1] * width - 2, hand[0] * height - 2,
                hand[1] * width + 2, hand[0] * height + 2
            ],
            fill=(hand_raised[i]*255, 0, hand_raised[i]*255))

    for sholder in sholders:
        draw.ellipse(
            xy=[
                sholder[1] * width - 2, sholder[0] * height - 2,
                sholder[1] * width + 2, sholder[0] * height + 2
            ],
            fill=(0, 0, 255))
    #img.save(args.output)
    #img.save(args.output)
    #print('Done. Results saved at', args.output)
    print(hand_raised)
    img.save("outo.jpg")
    return np.array(img),hand_raised[LEFT],hand_raised[RIGHT]



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


def drive(vehicle,left_hand, right_hand):
    # detect people

    p_location = 0
    p_size = 0

    # get location of the first person
    if left_hand or right_hand:

        if left_hand and right_hand:
            vehicle.set_vel(-0.99)


        elif left_hand:
            vehicle.set_vel(0.6)
            vehicle.turn(-0.2)

        elif right_hand:
            vehicle.set_vel(0.6)
            vehicle.turn(0.2)


    else:
        vehicle.stop()



import cv2

vehicle = vehicle_init()


# define a video capture object
vid = cv2.VideoCapture(1)

while (True):

    # Capture the video frame
    # by frame
    ret, inp = vid.read()

    pose ,left,right = det_pose(inp)
    # Display the resulting frame
    cv2.imshow('output',pose)
    drive(vehicle,left,right)


    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
