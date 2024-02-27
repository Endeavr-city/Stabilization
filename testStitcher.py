from testVideo import Stitcher

import numpy as np
import cv2
import imutils
import argparse
from imutils.video import VideoStream

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--first", required=True,
                help="C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CSCE 483 933/Stabilization/image1.png")
ap.add_argument("-s", "--second", required=True, 
                help="C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CSCE 483 933/Stabilization/image2.png")
args = vars(ap.parse_args())

# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
imageA = cv2.imread(args["first"])
imageB = cv2.imread(args["second"])
imageA = imutils.resize(imageA, width=400)
imageB = imutils.resize(imageB, width=400)

#stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)

#show the images
cv2.imshow("Image A", imageA)
cv2.imshow("Image B", imageB)
cv2.imshow("Keypoint Matches", vis)
cv2.imshow("Result", result)
cv2.waitKey(0)
"""
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
leftCamera.stop()
rightCamera.stop()
"""