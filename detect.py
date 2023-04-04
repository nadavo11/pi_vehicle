# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo which runs object detection on camera frames using GStreamer.

Run default object detection:
python3 detect.py

Choose different camera and input encoding
python3 detect.py --videosrc /dev/video1 --videofmt jpeg

TEST_DATA=../all_models
Run face detection model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_face_quant_postprocess_edgetpu.tflite

Run coco model:
python3 detect.py \
  --model ${TEST_DATA}/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite \
  --labels ${TEST_DATA}/coco_labels.txt
"""
import argparse

from periphery import GPIO

import gstreamer
import os
import time


from common import avg_fps_counter, SVG
from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference

from Vehicle import Vehicle
from motor import Motor


### import our vehicle

# from py_vehicle.v_init import vehicle
people=[]

def generate_svg(src_size, inference_box, objs, labels, text_lines):
    svg = SVG(src_size)
    src_w, src_h = src_size
    box_x, box_y, box_w, box_h = inference_box
    scale_x, scale_y = src_w / box_w, src_h / box_h

    for y, line in enumerate(text_lines, start=1):
        svg.add_text(10, y * 20, line, 20)
    for obj in objs:
        bbox = obj.bbox
        if not bbox.valid:
            continue
        # Absolute coordinates, input tensor space.
        x, y = bbox.xmin, bbox.ymin
        w, h = bbox.width, bbox.height
        # Subtract boxing offset.
        x, y = x - box_x, y - box_y
        # Scale to source coordinate space.
        x, y, w, h = x * scale_x, y * scale_y, w * scale_x, h * scale_y
        percent = int(100 * obj.score)
        label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))
        svg.add_text(x, y - 5, label, 20)
        svg.add_rect(x, y, w, h, 'red', 2)
    return svg.finish()


def main(termios=None):

    # default model path info.
    default_model_dir = '../pi_vehicle'
    default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite'
    default_labels = 'coco_labels.txt'
    
    """****************************************
                parse input args:
    ****************************************"""

    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='.tflite model path',
                        default=os.path.join(default_model_dir, default_model))
    parser.add_argument('--labels', help='label file path',
                        default=os.path.join(default_model_dir, default_labels))
    parser.add_argument('--top_k', type=int, default=8,
                        help='number of categories with highest score to display')
    parser.add_argument('--threshold', type=float, default=0.1,
                        help='classifier score threshold')
    parser.add_argument('--videosrc', help='Which video source to use. ',
                        default='/dev/video1')
    parser.add_argument('--videofmt', help='Input video format.',
                        default='raw',
                        choices=['raw', 'h264', 'jpeg'])
    parser.add_argument('--class', type = int, help='Input the object you would like to detect: for options check labels.txt',
                        default='0')
    args = parser.parse_args()
    args = parser.parse_args()

    # init TFlite things
    print('Loading {} with {} labels.'.format(args.model, args.labels))
    interpreter = make_interpreter(args.model)
    interpreter.allocate_tensors()
    labels = read_label_file(args.labels)
    inference_size = input_size(interpreter)

    # Average fps over last 30 frames.
    fps_counter = avg_fps_counter(30)


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
    """filedescriptors = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)
    x = 0"""

    def user_callback(input_tensor, src_size, inference_box):
        nonlocal fps_counter
        start_time = time.monotonic()
        run_inference(interpreter, input_tensor)

        """************************
        **************************"""
        # For larger input image sizes, use the edgetpu.classification.engine for better performance
        objs = get_objects(interpreter, args.threshold)[:args.top_k]

        ### detect people
        people = [obj for obj in objs if obj.id == 43]
        p_loc = 0
        p_size = 0
        if people:
            p = people[0]

            ### get location of the first person
            p_loc = (p.bbox.xmin + p.bbox.xmax - 300) / 2
            p_size = p.bbox.ymax-p.bbox.ymin
            print(f'person at : {p_loc}')


        end_time = time.monotonic()
        text_lines = [
            'Inference: {:.2f} ms'.format((end_time - start_time) * 1000),
            'FPS: {} fps'.format(round(next(fps_counter))),
        ]
        print(' '.join(text_lines))
        
        if people:
            if p_loc>60:
                vehicle.turn(0.9)
        
            elif p_loc < -60:
                vehicle.turn(-0.9)
            
#            if -50 < p_loc <50:
 #               vehicle.stop()
            else:
                if p_size < 100:
                    vehicle.set_vel(-0.9)
        
                elif p_size > 150:
                    vehicle.set_vel(0.9)
                else:
                    vehicle.stop()
        
        else:
            vehicle.stop()
        return generate_svg(src_size, inference_box, objs, labels, text_lines)

    result = gstreamer.run_pipeline(user_callback,
                                    src_size=(640, 480),
                                    appsink_size=inference_size,
                                    videosrc=args.videosrc,
                                    videofmt=args.videofmt)


    
if __name__ == '__main__':
    main()
 
