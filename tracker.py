# Some of this code is from a python tutorial site

# libraries to be downloaded
import cv2 # make sure you install opencv contrib from pip, not ordinary opencv
import numpy as np

# libraries that you dont need to dl
import winsound
import sys
import time
from math import dist
from math import acos
import math
import numpy
from datetime import datetime as dt
'''
'''
file_name = "video.mov" # change this line if using different video file
video = cv2.VideoCapture(file_name)
#video = cv2.VideoCapture(0) # uncomment this line to use real-time tracking 

output_path = ('balloon_data_' + str(time.time()) + '.csv')
video_fps = video.get(cv2.CAP_PROP_FPS)
conversion_factor = 57.295779 # used to convert from radians to degrees

print ("This video runs at a framerate of : {0}".format(video_fps))
print ("Outputting data to file:", output_path)

with open(output_path, "a") as text_file:
  print("elapsed_seconds_of_video", "actual_elapsed_seconds", "object_x_coordinate", "object_y_coordinate", "balloon_angle", "acceleration", sep=',', file=text_file)

def resize(img):
    # https://www.tutorialkart.com/opencv/python/opencv-python-resize-image/
    scale = 35
    new_w = int(img.shape[1] * scale / 100)
    new_h = int(img.shape[0] * scale / 100)
    dim = (new_w, new_h)
    return (cv2.resize(img, dim, interpolation = cv2.INTER_AREA))

def distance(x1, y1, x2, y2):
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
start_time = time.time()

if __name__ == '__main__' :
    # Set up tracker.
    # Instead of CSRT, you can also use
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']
    #                   0         1     2      3       4           5           6        7
    tracker_type = tracker_types[7]
    # it is recommended to use 7
    # the other tracker types do not work as well
    print("Using tracker type: ", tracker_type)
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        elif tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        elif tracker_type == 'KCF':
            tracker = cv2.legacy.TrackerKCF_create()
        elif tracker_type == 'TLD':
            tracker = cv2.legacy.TrackerTLD_create()
        elif tracker_type == 'MEDIANFLOW':
            tracker = cv2.legacy.TrackerMedianFlow_create()
        elif tracker_type == 'GOTURN':
             tracker = cv2.legacy.TrackerGOTURN_create()
        elif tracker_type == 'MOSSE':
            tracker = cv2.legacy.TrackerMOSSE_create()
        elif tracker_type == "CSRT":
            tracker = cv2.TrackerCSRT_create()

# Read video
cntr = 0.0
def mainLoop(cntr):
  # Exit if video not opened.
  if not video.isOpened():
    print("Could not open video")
    sys.exit()

  # Read first frame.
  ok, frame = video.read()
  frame = resize(frame);
  if not ok:
    print ('Cannot read video file')
    sys.exit()

  # Define an initial bounding box
  # For instance:
  # bbox = (100, 400,         160, 410)
  #         x1   y1           x2   y2
  cv2.putText(frame, tracker_type + " Choose Balloon Point", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2);
  bbox = cv2.selectROI(frame, True)
  print("Bounding Box: ", bbox)

  ok, frame = video.read()
  frame = resize(frame);
  if not ok:
    print ('Cannot read video file')
    sys.exit()

  cv2.putText(frame, tracker_type + " Choose Anchor Point", (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,255),2);
  bbox2 = cv2.selectROI(frame, True)
  print("Bounding Box: ", bbox2)

  p1 = (int(bbox[0]), int(bbox[1]))
  p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

  # Initialize tracker with first frame and bounding box

  height, width = frame.shape[:2]
  orig_x = int((p1[0]+p2[0])/2.0)
  orig_y = int((p1[1]+p2[1])/2.0)

  p1b = (int(bbox2[0]), int(bbox2[1]))
  p2b = (int(bbox2[0] + bbox2[2]), int(bbox2[1] + bbox2[3]))

  anchor_x = int((p1b[0]+p2b[0])/2.0)
  anchor_y = int((p1b[1]+p2b[1])/2.0)

  ok = tracker.init(frame, bbox)
  prev_angle = -1.00

  cntr += 2.00
  while True:
       ok, frame = video.read()

       if not ok:
           break

       frame = resize(frame)
       timer = cv2.getTickCount()
       ok, bbox = tracker.update(frame)
       cur_time = time.time() - start_time
       fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

       if ok:
           p1 = (int(bbox[0]), int(bbox[1]))
           p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

           centroid_x = int((p1[0]+p2[0])/2.0)
           centroid_y = int((p1[1]+p2[1])/2.0)
           angle = -1.00

           A = distance(centroid_x, centroid_y, anchor_x, anchor_y)
           B = distance(anchor_x, anchor_y, anchor_x, centroid_y)
           C = distance(anchor_x, centroid_y, centroid_x, centroid_y)

           if ((math.isnan(C)) or (math.isnan(B)) or (abs(B - 0.000) <= 0.01)):
             acceleration = -1.00
           else:
             angle = (np.arctan(C/B))
             acceleration = (math.tan((2*angle)))*9.81

           cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
           cv2.circle(frame, (centroid_x, centroid_y), 2, (0, 0, 255), 5)
           cv2.circle(frame, (anchor_x, anchor_y), 2, (255, 0, 0), 5)
           cv2.line(frame, (centroid_x, centroid_y), (anchor_x, anchor_y), (255, 0, 0), 1)
           cv2.line(frame, (anchor_x, anchor_y), (anchor_x, centroid_y), (255, 0, 0), 1)
           cv2.line(frame, (anchor_x, centroid_y), (centroid_x, centroid_y), (255, 0, 0), 1)

           AcceptableAngleJump = True
           maxThreshold = 45

           if ((prev_angle == -1.00) or (int(prev_angle) == int(-1))):
            prev_angle = angle
           else:
             #print("Frame-to-frame change in angle:", abs(angle-prev_angle))
             if (abs((angle*conversion_factor)-(prev_angle*conversion_factor)) > 45):
               AcceptableAngleJump = False
             prev_angle = angle

           isValid = ((AcceptableAngleJump) and (int(angle*conversion_factor) <= 89) and (angle > 0) and (int(angle) != -1) and (abs(acceleration) <= maxThreshold) and (acceleration >= 0))
           # If there's a sudden jump in angle or if the angle value is nonsensical, no data will be outputted

           if (isValid):
             cv2.putText(frame, ("Angle: "+ str(round(angle*conversion_factor,3)) + " deg."), (abs(anchor_x-40),anchor_y), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
             cv2.putText(frame, ("Accel: "+ str(round(acceleration,3)) + " m/s^2"), (abs(anchor_x-40),anchor_y+50), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

             print("Elapsed seconds in video, balloon angle (degrees), acceleration (m/s^2): ", end="")
             print(round((cntr+1.0)/video_fps, 5), round(angle*conversion_factor, 5), round(acceleration, 5), sep=',')
             with open(output_path, "a") as text_file:
               print((cntr+1.0)/video_fps, cur_time, centroid_x, centroid_y, angle*conversion_factor, acceleration, sep=',', file=text_file)

       else:
           cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

       # Display tracker type on frame
       cv2.putText(frame, "Frames Elapsed: " + str(cntr), (80,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
       # Display FPS on frame
       cv2.putText(frame, "FPS : " + str(int(fps)), (80,40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);
       # Display result
       cv2.imshow("Tracking", frame)
       cntr += 1.0
       # Exit if ESC pressed
       if cv2.waitKey(1) & 0xFF == ord('q'): # if press SPACE bar
         print("q has been pressed")
         return cntr;

try:
  cntr = mainLoop(cntr);
  while True:
    cntr = mainLoop(cntr);

finally:
  video.release()
  cv2.destroyAllWindows()

  # Play beep sound once program is done
  # Only works on windows
  duration = 1000
  freq = 250
  winsound.Beep(freq, duration)
