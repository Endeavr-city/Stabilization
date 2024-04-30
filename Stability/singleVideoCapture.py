#Python program to save an operated video 

#import cv2 and numpy for processing 
import numpy as np
import cv2 
                                      
#This will return video from camera0, or camera 1 on the computer, which is either the webcam or the attached camera
cap = cv2.VideoCapture(2)                                                                            #0 is for webcam, 1 is for the attached camera 
#Extract frames, width and height for the video 
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Define the codec and create VideoWriter object
#This specific code is derived from the current stability code reference page
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
#out = cv2.VideoWriter(
    #'stabilized_video.mp4',
    #fourcc, 
   # fps, 
  #  (2 * width, height)
#)
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc,fps,(2 * width, height))
#Note: Video will likely output a corruput video file if the fps, width and height is incorrect and not of the correct, proper resolution
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('RetroPilotFiles/testVid.mp4', #label the correct folder within which video will be placed
#                       fourcc, 
#                       fps, 
#                       (int(width), int(height)))

#loop runs if capturing has been initialized 
while (True):
    #reads frames from the camera 
    #ret checks return at each frame 
    ret, frame = cap.read()

    #Converts to grayscale space, OCV reads colors as BGR
    #frame is converted to gray 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #output the frame
    # out.write(frame)

    #The original input frame is shown in the window
    cv2.imshow('Original', frame)
    
    #The window showing the operated video stream 
    # cv2.imshow('frame', gray)

    #Wait for 'q' key to stop the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Close the window / Release camera 
cap.release()
# out.release()

#After we release the webcam, we also release the out-out.release()
cv2.destroyAllWindows()