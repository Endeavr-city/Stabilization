#import required libraries
#from vidgear.vidgear.gears import WriteGear
#from vidgear.vidgear.gears.stabilizer import Stabilizer
#following are imports to test on Orin 
from vidgear.gears import WriteGear
from vidgear.gears.stabilizer import Stabilizer
import cv2 
import time #Importing time to record the latency captured

#Open the specific video stream, with webcam index here
stream = cv2.VideoCapture(0) #for getting camera feed

#initiate the stabilizer object with defined parameters
#regular normal parameters used, initial smoothing r=30, border_size = 5
stab = Stabilizer(smoothing_radius=20, crop_n_zoom=True, border_size=5, logging=True)

#might not use writeGear here
#Extract frames, width and height for the video 
fps = stream.get(cv2.CAP_PROP_FPS)
width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

#Latency computation
endLatency = 0 #variable that will compute the latency for the stability, between before when each frame is stabilized, and after it is output
latencies = [] #sotres all the latencies computed per frame
#Specify the output format of the video, so that the correct width and height can be outputted
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#following line is the local path for storing videos tested on PC, in this case the orin, specify the output correctly
out = cv2.VideoWriter('/home/orin/Desktop/RetroPilotFiles/demoTesting/latencyOutput4.mp4',
                      fourcc, 
                      fps, 
                      (int(width), int(height))) #Need to multiply twice the width, in order to capture proper frame size, fixed this with this change


# loop over
while True:

    # read frames from stream
    #frame = stream.read()- needs to be changed, to specify openCV input
    (grabbed, frame) = stream.read() 

    #check for frame is not grabbed
    if not grabbed: 
        break
    
    #Converts to grayscale space, OCV reads colors as BGR
    #frame is converted to gray 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #start variable, which will record the frame capture, right before the stabilized frame is captured
    start = time.perf_counter()    

    # send current frame to stabilizer for processing
    stabilized_frame = stab.stabilize(frame)

    # wait for stabilizer which still be initializing
    if stabilized_frame is None:
        continue

    # store the output frame, as the stabilized frame here
    output_frame = stabilized_frame

    #Show the combined output window, showing original video and stabilized video side by side
    cv2.imshow('output_frame', output_frame)

    #endlatency that will record the computation difference from start, and the current time counter, which is the computed latency
    endLatency = time.perf_counter() - start
    print('{:.6f}s latest latency for frames'.format(endLatency)) #latency output
    latencies.append(endLatency) #append each latency to the latencies list
    #cv2.waitKey(10)

    # Write to the output frame using OpenCV 
    out.write(output_frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

totalSum = 0 #store all latencies in a total sum
for latency in latencies: 
    totalSum += latency #go in a loop and sum all the latencies together

avg_latency = totalSum / len(latencies) #at the end compute the avg latency, and output accordingly
print('{:.6f}s  avg latency'.format(avg_latency)) # print out the average latency as required

# clear stabilizer resources
stab.clean()

# safely close video stream
stream.release()
#Release the camera
out.release()

# close output window
cv2.destroyAllWindows()

