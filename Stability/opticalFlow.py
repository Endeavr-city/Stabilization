import cv2
import numpy as np

#cap = cv2.VideoCapture("C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CapstoneFiles/Stabilization/StabilizedOutput/stabilized_video_v2.mp4") #put in file path
cap = cv2.VideoCapture("C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CapstoneFiles/CAPSTONE_IMUTesting/UncompressedVids/raw_run2_stabilized.avi")
#getting first frame of video
ok, frame = cap.read()

#Generate intial corners of detected object
#Set limit, minimum distance in pixels, and quality of object corner to be tracked
parameters_shitomasi = dict(maxCorners=100, qualityLevel=0.3, minDistance=7)

#convert to grayscale
frame_gray_init = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#Use Shi-Tomasi to detect object corners/edges from initial frame
edges = cv2.goodFeaturesToTrack(frame_gray_init, mask = None, **parameters_shitomasi)

#Create black canavas the size of initial frame
canvas = np.zeros_like(frame)
colours = np.random.randint(0, 255, (100, 3))

#set min size of tracked object
parameter_lucas_kanade = dict(winSize=(15,15), maxLevel=2, criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


#loop for all frames
while True: 
    #get next frame
    ok, frame = cap.read()
    if not ok: 
        print("[INFO] end of file reached")
        break 
    
    #prepare greyscale image
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #update object corners by comparing with found edges in initial frame
    update_edges, status, errors = cv2.calcOpticalFlowPyrLK(frame_gray_init, frame_gray, edges, None, **parameter_lucas_kanade)
  
    #only update edges  if algorithm successfully tracked
    new_edges = update_edges[status == 1]
    # to calculate directional flow we need to compare with previous position
    old_edges = edges[status == 1]
    for i, (new, old) in enumerate(zip(new_edges, old_edges)):
        a, b = new.ravel()
        c, d = old.ravel()
        
        #draw line between old and new corner point with random color
        mask = cv2.line(canvas, (int(a), int(b)), (int(c), int(d)), colours[i].tolist(), 2)
        # draw circle around new position
        frame = cv2.circle(frame, (int(a), int(b)), 5, colours[i].tolist(), -1)
        
    # add frame and masking onto result
    result = cv2.add(frame, mask)
    # and then apply optical flow onto the result
    cv2.imshow('Optical Flow (sparse)', result)
    # if possible, press q to exit the program
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    #overrite initial frame with current before restarting the loop
    frame_gray_init = frame_gray.copy()
    #update to new edges before restarting the loop
    edges = new_edges.reshape(-1, 1, 2)
    
# release the frame capture and clean-up as needed
cap.release()
cv2.destroyAllWindows()