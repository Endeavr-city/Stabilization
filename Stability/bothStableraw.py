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
stream_2 = cv2.VideoCapture(2) #for getting camera feed from second camera

#process the frames, width and height
fps = stream.get(cv2.CAP_PROP_FPS)
width = int(stream.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(stream.get(cv2.CAP_PROP_FRAME_HEIGHT))

#used to record the time when we processed last frame
prev_frame_time = 0

#used to record the time at which we processed current frame
new_frame_time = 0

#Latency computation
endLatency = 0 #variable that will compute the latency for the stability, between before when each frame is stabilized, and after it is output
latencies = [] #sotres all the latencies computed per frame
#Specify the output format of the video, so that the correct width and height can be outputted
out = cv2.VideoWriter(
    #'/home/orin/Desktop/RetroPilotFiles/VidGearTestFiles/latencyOutput.mp4',
    '/home/orin/Desktop/RetroPilotFiles/finalDemoTesting/bothStable_smooth_raw.avi',
    #'highway_day1_mask.avi', 
    cv2.VideoWriter_fourcc(*'XVID'), fps, (2* int(width), int(height)))

#while true, process both frames
while True:
    #process the first frame, for camera 1, which is the left camera
    ret, frame = stream.read()
    #Error check for first frame
    if not ret:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    #process the second frame, for camera 2, which is the right camera
    ret_2, frame_2 = stream_2.read()
    #Error check for the second frame
    if not ret_2: 
        print("Frame 2: video frame is empty or video processing has been successfully completed.")

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()

    #start variable, which will record the frame capture, right before the stabilized frame is captured
    start = time.perf_counter()    

    # concatenate both raw frames
    concat_frame = cv2.hconcat([frame, frame_2])
    # Calculating the fps 
    # fps will be number of frame processed in given time frame 
    # since their will be most of time error of 0.001 second 
    # we will be subtracting it to get more accurate result 
    fps_internal = 1/(new_frame_time-prev_frame_time) 
    prev_frame_time = new_frame_time 

    # converting the fps into integer
    fps_internal = int(fps_internal)

    #converting the fps to string, so that we can display it on the frame by using putText function
    fps_internal = str(fps_internal)

    # putting the FPS count on the frame
    cv2.putText(concat_frame, fps_internal, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    # displaying the frame with fps
    #cv2.imshow("instance-segmentation", output_frame)

    #endlatency that will record the computation difference from start, and the current time counter, which is the computed latency
    endLatency = time.perf_counter() - start
    print('{:.6f}s latest latency for frames'.format(endLatency)) #latency output
    latencies.append(endLatency) #append each latency to the latencies list
    #cv2.waitKey(10)

    out.write(concat_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


totalSum = 0 #store all latencies in a total sum
for latency in latencies: 
    totalSum += latency #go in a loop and sum all the latencies together

avg_latency = totalSum / len(latencies) #at the end compute the avg latency, and output accordingly
print('{:.6f}s  avg latency'.format(avg_latency)) #print out the latency

# safely close video stream
stream.release()
#Release the camera
out.release()
#cap.release()
cv2.destroyAllWindows()
