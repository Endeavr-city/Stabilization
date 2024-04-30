import cv2
#from ultralytics import YOLO
#from ultralytics.utils.plotting import Annotator, colors
#import required libraries
#from vidgear.vidgear.gears import WriteGear
#from vidgear.vidgear.gears.stabilizer import Stabilizer
#following are imports to test on Orin 
#from vidgear.gears import WriteGear
from vidgear.gears.stabilizer import Stabilizer
#import cv2 
import time #Importing time to record the latency captured

#Open the specific video stream, with webcam index here
stream = cv2.VideoCapture(0) #for getting camera feed

# process the width, height and frames accordingly
w, h, fps = (int(stream.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))


#Latency computation
endLatency = 0 #variable that will compute the latency for the stability, between before when each frame is stabilized, and after it is output
latencies = [] #sotres all the latencies computed per frame
#Specify the output format of the video, so that the correct width and height can be outputted
out = cv2.VideoWriter(
    '/home/orin/Desktop/RetroPilotFiles/finalDemoTesting/oneRaw_smooth.avi',
    #'highway_day1_mask.avi',
      cv2.VideoWriter_fourcc(*'XVID'), fps, (w, h))

# while true, process all frames
while True:
    # read the frames one by one
    ret, frame = stream.read()
    # Error-check if frame-reading fails
    if not ret:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    #start variable, which will record the frame capture, right before the stabilized frame is captured
    start = time.perf_counter()    

    #endlatency that will record the computation difference from start, and the current time counter, which is the computed latency
    endLatency = time.perf_counter() - start
    print('{:.6f}s latest latency for frames'.format(endLatency)) #latency output
    latencies.append(endLatency) #append each latency to the latencies list
    #cv2.waitKey(10)

    # Write the frame to the output
    out.write(frame)

    # if possible, type q to exit the program, or ctrl-c in the terminal to do so
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


totalSum = 0 #store all latencies in a total sum
for latency in latencies: 
    totalSum += latency #go in a loop and sum all the latencies together

avg_latency = totalSum / len(latencies) #at the end compute the avg latency, and output accordingly
print('{:.6f}s  avg latency'.format(avg_latency)) #print out the avg latency

# safely close video stream
stream.release()
#Release the camera
out.release()
#cap.release()
cv2.destroyAllWindows()
