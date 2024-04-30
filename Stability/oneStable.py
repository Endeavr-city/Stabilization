import cv2
from ultralytics import YOLO
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

#initiate the stabilizer object with defined parameters
#regular normal parameters used, initial smoothing r=30, border_size = 5
stab = Stabilizer(smoothing_radius=18, crop_n_zoom=True, border_size=5, logging=False)

#Initialize the model to be used for segmentation
model = YOLO("bestv2_1_coco.pt")

# process the frame-rate, width and height
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
    '/home/orin/Desktop/RetroPilotFiles/finalDemoTesting/oneStable_people.avi',
    #'/home/orin/Desktop/RetroPilotFiles/VidGearTestFiles/latencyOutput.mp4',
    #'highway_day1_mask.avi', 
    cv2.VideoWriter_fourcc(*'XVID'), fps, (int(width), int(height)))

# While true, read frames from camera 1 and 2
while True:
    # read from camera 1, left camera
    ret, frame = stream.read()
    # Error-check if frame-reading fails
    if not ret:
        print("Video frame is empty or video processing has been successfully completed.")
        break

    # font which we will be using to display FPS
    font = cv2.FONT_HERSHEY_SIMPLEX
    # time when we finish processing for this frame
    new_frame_time = time.time()

    #start variable, which will record the frame capture, right before the stabilized frame is captured
    start = time.perf_counter()    

    # send current frame to stabilizer for processing
    stabilized_frame = stab.stabilize(frame)

    # Send stabilized frame to segmentation model
    results = model.predict(stabilized_frame, conf=0.6)
    annotated_frame = results[0].plot(boxes=True)

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
    cv2.putText(annotated_frame, fps_internal, (7, 70), font, 3, (100, 255, 0), 3, cv2.LINE_AA)

    #cv2.imshow("instance-segmentation", stabilized_frame)

    #endlatency that will record the computation difference from start, and the current time counter, which is the computed latency
    endLatency = time.perf_counter() - start
    print('{:.6f}s latest latency for frames'.format(endLatency)) #latency output
    latencies.append(endLatency) #append each latency to the latencies list
    #cv2.waitKey(10)

    # write stabilized and segmented frame onto output
    out.write(annotated_frame)

    # if possible, press q to exit the program, else Ctrl-C in the terminal to do so
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


totalSum = 0 #store all latencies in a total sum
for latency in latencies: 
    totalSum += latency #go in a loop and sum all the latencies together

avg_latency = totalSum / len(latencies) #at the end compute the avg latency, and output accordingly
print('{:.6f}s  avg latency'.format(avg_latency)) # print out the average latency


# safely close video stream
stream.release()
#Release the camera
out.release()
#cap.release()
cv2.destroyAllWindows()
