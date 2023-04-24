
import argparse
from PIL import Image
from PIL import ImageDraw
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter
_NUM_KEYPOINTS = 17


def main(input):
def det_pose(input):
  parser = argparse.ArgumentParser(
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument(
      '-m', '--model', required=True, help='File path of .tflite file.')
  #parser.add_argument(
  #    '-i', '--input', required=True, help='Image to be classified.')
  #parser.add_argument(
  #    '--output',
  #    default='movenet_result.jpg',
  #    help='File path of the output image.')
  args = parser.parse_args()
  interpreter = make_interpreter(args.model)
  interpreter.allocate_tensors()
  img = Image.open(input)
  resized_img = img.resize(common.input_size(interpreter), Image.ANTIALIAS)
  common.set_input(interpreter, resized_img)
  interpreter.invoke()
  pose = common.output_tensor(interpreter, 0).copy().reshape(_NUM_KEYPOINTS, 3)
  print(pose)
  draw = ImageDraw.Draw(img)
  width, height = img.size
  for i in range(0, _NUM_KEYPOINTS):
    draw.ellipse(
        xy=[
            pose[i][1] * width - 2, pose[i][0] * height - 2,
            pose[i][1] * width + 2, pose[i][0] * height + 2
        ],
        fill=(255, 0, 0))
  img.save(args.output)
  print('Done. Results saved at', args.output)
  return img
import cv2
# define a video capture object
vid = cv2.VideoCapture(1)
while (True):
    # Capture the video frame
    # by frame
    ret, input = vid.read()

    # Display the resulting frame
    cv2.imshow('output',main(input))
    cv2.imshow('output',det_pose(input))

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()