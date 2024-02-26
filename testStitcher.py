from testVideo import Stitcher

import numpy as np
import cv2
import imutils
from imutils.video import VideoStream


#initialize video streams and warmup
print("Getting Camera Feeds...")
leftCamera = VideoStream(src=1).start()
rightCamera = VideoStream(src=2).start()

#initialize stitcher program
stitcher = Stitcher()

while True:
    #Read camera feed from both cameras
    left = leftCamera.read()
    right = rightCamera.read()

    #Stitch the two videos together to form panorama
    result = stitcher.stitch([left,right])

    #if no homography can be computed break the program
    if result is None:
        print("Homography could not be computed")
        break

    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == ord('q'): #If 'q' is pressed it will kill the programe
        break

cv2.destroyAllWindows()
leftCamera.stop()
rightCamera.stop()
