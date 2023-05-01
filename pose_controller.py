
import argparse

import numpy as np
from PIL import Image
from PIL import ImageDraw
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
import numpy as np
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


   # print(pose)
    draw = ImageDraw.Draw(img)
    width, height = img.size
    hands = pose[9:11]
    sholders = pose[5:7]

    hand_raised[RIGHT] = hands[RIGHT, 0] < sholders[RIGHT, 0]
    hand_raised[LEFT] = hands[LEFT, 0] < sholders[LEFT, 0]
    for i, hand in enumerate(hands):
        draw.ellipse(
            xy=[
                hand[1] * width - 6, hand[0] * height - 6,
                hand[1] * width + 6, hand[0] * height + 6
            ],
            fill=(hand_raised[i]*255, 0,255- hand_raised[i]*255))

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
   # img.save("outo.jpg")
    print(hand_raised)
    return np.array(img)


import cv2

# define a video capture object
vid = cv2.VideoCapture(1)

while (True):

    # Capture the video frame
    # by frame
    ret, inp = vid.read()

    # Display the resulting frame
    cv2.imshow('output',det_pose(inp))

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
