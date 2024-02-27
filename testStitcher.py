from testVideo import Stitcher

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
#image = cv2.imread("image1.png")
aa = cv2.imread("image1.png",cv2.IMREAD_COLOR)
bb = cv2.imread("image2.png",cv2.IMREAD_COLOR)
#leftCamera = VideoStream(src=1).start()
#rightCamera = VideoStream(src=2).start()
leftCamera = cv2.VideoCapture(0)  # 첫 번째 카메라
rightCamera = cv2.VideoCapture(2)  # 두 번째 카메라

#initialize stitcher program
stitcher = Stitcher()
# result=leftCamera.read()[1]
# result_2=rightCamera.read()[1]

while True:
    #Read camera feed from both cameras
    _, left = leftCamera.read()
    _, right = rightCamera.read()
    #left = aa
    #right = bb

    #frame re-sizing
    #left = imutils.resize(left, width=400)
    #right = imutils.resize(right, width=400)

    #Stitch the two videos together to form panorama
    result = stitcher.stitch([left,right])

    #if no homography can be computed break the program
    if result is None:
        print("Homography could not be computed")
        break
    break
# 이미지 저장
cv2.imwrite('resized_image.jpg', result)
exit()
    # cv2.imshow("Result", result)

    # if cv2.waitKey(1) & 0xFF == ord('q'): #If 'q' is pressed it will kill the programe
    #     break

#do the cleanup portion here to stop processing 
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
#leftCamera.stop()
#rightCamera.stop()
