import numpy as np
import cv2

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

cv2.destroyAllWindows()