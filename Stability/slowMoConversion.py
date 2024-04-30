#Import require modules for openCV2 in order to convert the video into a slow-motion video
import cv2 

#return a video saved at the specific location 
cap = cv2.VideoCapture("C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CapstoneFiles/CAPSTONE_IMUTesting/raw_run7.avi") #Enter the path of the video here

#Specify the source variable and create a VideoWriter object
#fps here determines the framerate of the output video
#it will be passed to VideoWriter object
#Note that lower the frame rate slower in the video 
#fps = 5.0

#retrieve dimensions for height and width from the video frame
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#fps is already set above to a lower frame speed for processing
#Else retrieve the fps speed from the video, and adjust via waitKey
fps = 2
#fps = cap.get(cv2.CAP_PROP_FPS)
# specify the path,. video-writer object format, and the proper output for the video
path = "C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CapstoneFiles/CAPSTONE_IMUTesting/UncompressedVids/raw_slow_run7.avi" #path for slowed-down video 
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter(path, fourcc, 2, (int(width), int(height)))

#for higher-playback speed, export a higher frame-rate speed of 40 fps, fps = 40.0
#create the infinite loop to read the VideoCapture object frame by frame, specify a key value using waitKey to break out of the loop
while True: 
    #reading the cap object for a single frame of video 
    ret, frame = cap.read()
    #for displaying the frame read from a cap object
    cv2.imshow("frame", frame) 

    #using the VideoWriter object output for writing the frame into the output video 
    output.write(frame)

    #waitKey specifies the value in millisecond for which a particular frame, in this case we set it to 24
    k = cv2.waitKey(24)

    # if 'q' is pressed then above while loop will break video reading and writing, process will stop
    if k == ord("q"): 
        break

#release the cap, close the output and all windows captured 
cap.release()
output.release()
cv2.destroyAllWindows()