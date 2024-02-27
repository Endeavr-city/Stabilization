from testVideo import Stitcher

import numpy as np
import cv2
import imutils
import argparse
from imutils.video import VideoStream

#show the images
"""image = cv2.imread("image1.png")
aa = cv2.imread("image1.png",cv2.IMREAD_COLOR)
bb = cv2.imread("image2.png",cv2.IMREAD_COLOR)
cv2.imshow("frame1",aa)
cv2.imshow("frame2",bb)
"""
#initialize video streams and warmup
print("Getting Camera Feeds...")
#image = cv2.imread("image1.png")
aa = cv2.imread("image1.png",cv2.IMREAD_COLOR)
bb = cv2.imread("image2.png",cv2.IMREAD_COLOR)
#leftCamera = VideoStream(src=1).start()
#rightCamera = VideoStream(src=2).start()

#initialize stitcher program
stitcher = Stitcher()

while True:
    #Read camera feed from both cameras
    #left = leftCamera.read()
    #right = rightCamera.read()
    left = aa
    right = bb

    #frame re-sizing
    #left = imutils.resize(left, width=400)
    #right = imutils.resize(right, width=400)

    #Stitch the two videos together to form panorama
    result = stitcher.stitch([left,right])

    #if no homography can be computed break the program
    if result is None:
        print("Homography could not be computed")
        break

    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == ord('q'): #If 'q' is pressed it will kill the programe
        break

#do the cleanup portion here to stop processing 
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
#leftCamera.stop()
#rightCamera.stop()
