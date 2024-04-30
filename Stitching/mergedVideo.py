import cv2
import numpy as np
import time
#from imutils.video import VideoStream
from siftVideo import Stitcher  
#from vidGearWithFeedCapture import vidGearFeed #imported from vidGearFeed
#from vidgear.vidgear.gears.stabilizer import Stabilizer #import stabilizer for PC
from vidgear.gears.stabilizer import Stabilizer #for orin

class MergedVideo:
    def __init__(self):
        # Initialize the video streams for two cameras
        print("[INFO] Starting video streams...")
        #Orin settings for camera
        self.stream1 = cv2.VideoCapture(0) #Changed for Open-CV processing
        self.stream2 = cv2.VideoCapture(2) #Change to 2 for Orin
        #for PC
        # self.stream1 = cv2.VideoCapture(1) #Changed for Open-CV processing
        # self.stream2 = cv2.VideoCapture(0)

        # adjust the freame rate, width and height accordingly
        self.fps = self.stream1.get(cv2.CAP_PROP_FPS)
        self.width = int(self.stream1.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.stream1.get(cv2.CAP_PROP_FRAME_HEIGHT))

        #Specify the output format of the video
        self.out = cv2.VideoWriter(
        #'/home/orin/Desktop/RetroPilotFiles/VidGearTestFiles/latencyOutput.mp4',
        '/home/orin/Desktop/RetroPilotFiles/finalDemoTesting/stitcher_car1.avi',
        #'highway_day1_mask.avi',  
        cv2.VideoWriter_fourcc(*'XVID'), self.fps, (2*int(self.width), int(self.height)))


        # Initialize the Stitcher12
        self.stitcher = Stitcher()
        #self.output = vidGearFeed() #Declare the vidGear feed object
        self.stab = Stabilizer(smoothing_radius=8, crop_n_zoom=True, border_size=8, logging=True)

    # define the run function with self as the input
    def run(self):
        # Initialize variables for FPS calculation
        fpsReport = 0
        frameCount = 0
        startTime = time.time()

        # while true, capture frames from both cameras
        while True: 
            # grab frames from both camera 1 and 2
            (grabbed1, frame1) = self.stream1.read()
            (grabbed2, frame2) = self.stream2.read()

            #check for frame is not grabbed
            if not grabbed1: 
                break

            if not grabbed2: 
                break

            # Check if frames are grabbed
            if frame1 is None or frame2 is None:
                print("Failed to grab frames.")
                break

            # Stitch the frames together
            raw_input = self.stitcher.stitch([frame1, frame2])
            raw_input = cv2.resize(raw_input, (2 * int(self.width), int(self.height)))

            #Alternate method, where we stabilize both, and then stitch frames to get output
            # frame1 = self.stab.stabilize(frame1)
            # frame2 = self.stab.stabilize(frame2)
            # result = self.stitcher.stitch([frame1,frame2])

            #Non-stitching method to stack the frames together, without stitching
            # Using numpy hstack
            #result = np.hstack((frame1,frame2))
            #raw_input = np.hstack((frame1,frame2))
            # Using conacatenation- hconcat
            # result = cv2.hconcat([frame1,frame2])
            # raw_input = cv2.hconcat([frame1,frame2])

            #stabilize the resultant frames
            #result = self.stab.stabilize(result)

            if raw_input is not None:
                # Calculate and display FPS
                frameCount += 1
                if frameCount == 10:
                    endTime = time.time()
                    fpsReport = 10 / (endTime - startTime)
                    startTime = time.time()
                    frameCount = 0
                
                # Display FPS on the stitched frame
                cv2.putText(raw_input, "FPS: {:.2f}".format(fpsReport), (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # output the stitched result
                cv2.imshow('stitched_result', raw_input)
            
            # Break loop with 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Stop video streams and close windows
        self.stream1.release()
        self.stream2.release()
        cv2.destroyAllWindows()

# run both functions in main
if __name__ == "__main__":
    mergedVideo = MergedVideo()
    mergedVideo.run()

