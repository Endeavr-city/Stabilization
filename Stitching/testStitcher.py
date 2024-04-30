from siftVideo import Stitcher

import numpy as np
import cv2
import imutils
import argparse

#show the images
"""image = cv2.imread("image1.png")
aa = cv2.imread("image1.png",cv2.IMREAD_COLOR)
bb = cv2.imread("image2.png",cv2.IMREAD_COLOR)
cv2.imshow("frame1",aa)
cv2.imshow("frame2",bb)
"""
#initialize video streams and warmup
print("Getting Camera Feeds...")
aa = cv2.imread("image1.png",cv2.IMREAD_COLOR)
bb = cv2.imread("image2.png",cv2.IMREAD_COLOR)

#initialize stitcher program
stitcher = Stitcher()
# while true, capture frames from both cameras
while True:
    left = aa
    right = bb

    #Stitch the two videos together to form panorama
    result = stitcher.stitch([left,right])

    #if no homography can be computed break the program
    if result is None:
        print("Homography could not be computed")
        break
    
    # display the result in the view
    cv2.imshow("Result", result)

    if cv2.waitKey(1) & 0xFF == ord('q'): #If 'q' is pressed it will kill the programe
        break
# clean up as needed
cv2.destroyAllWindows()
