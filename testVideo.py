import numpy as np
import cv2
import imutils

class Stitcher:
    def __init__(self):
        self.isv3 = imutils.is_cv3() #determine if using latest openCV version and initialize cahced homography matrix
        self.cachedH = None

        def stitch(self, images, ratio=0.75, reprojThresh = 4.0):
            #unpack images
            (imageB, imageA) = images

            if self.cachedH is None:
                #find keypoints and extract
                (kpsA, featuresA) = self.detectAndDescribe(imageA)
                (kpsB, featuresB) = self.detectAndDescribe(imageB)

                #match features between images
                M = self.matchKeyPoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)

                #if no match then return nothing
                if M is None:
                    return None
                
                #cache the homography matrix
                self.cachedH = M[1]

            #apply perspective transform to stitch images together using homography matrix
            result = cv2.warpPerspective(imageA, self.cachedH, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

            result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

            #return stitched image
            return result


"""
vid1 = cv2.VideoCapture(1) #Get Video feed from Camera 1
vid2 = cv2.VideoCapture(2) #Get video feed from Camera 2

while (True):
    ret1, frame1 = vid1.read() #reads the frames from Camera 1 
    ret2, frame2 = vid2.read() #reads the frames from Camera 2

    frame = cv2.hconcat([frame1, frame2]) #Concatenates the two video feeds side by side

    cv2.imshow('frame', frame) #Displays the camera videos

    if cv2.waitKey(1) & 0xFF == ord('q'): #If 'q' is pressed it will kill the programe
        break

vid1.release()
vid2.release()

cv2.destroyAllWindows()"""