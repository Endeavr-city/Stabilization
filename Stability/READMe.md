For Video Stability, we have provided a brief summary of the contents of each code file below-
1. bothStable.py - Extracts stabilized video feed from two cameras (non-stitched), and outputs the video. 
2. bothStableRaw.py - Extracts raw, non-stabilized video feed from two cameras (non-stitched), and outputs the video. 
3. dualCamStream.py - Alternate implementation of stabilizing video and outputtin from two cameras (non-stitched).
4. oneRaw.py - Simply extracts raw, non-stabilized video feed from one camera, and outputs the video. 
5. opticalFlow.py - Draws an optical-flow line for each video stream, to keep track of the displacement of objects in the frame, for each successive frame. For further reference regarding the open source optical flow, used, plese refer to additional links provided below.
6. singleVideoCapture.py - Captures non-stabilized video feed from a single camera, and outputs video to screen. 
7. slowMoConversion.py - Alternate attempt to reduce the number of frame rate of a video, during video playback. Intent is to decrease the video playback speed. 
8. stability.py - Alternate open-source based implementation of video-stability, that does not use VidGear, and relies on opencV. For further info, please refer to sources below. 
9. testIMU.py - Collects acceleration and gyroscope data from an MPU chip, and writes to a CSV file. 
10. vidGearWithFeed.py - Uses VidGear's video stream capture method to capture and record stabilized footage. Utilizes VidGear stabilization algorithm for video stability. 
11. vidGearWithFeedCapture.py - Uses openCV's video stream capture method to capture and record stabilized footage. Utilizes VidGear stabilization algorithm for video video stability. 
12. setup.py - VidGear setup file. Refer to videgear documentation for understanding. 

Important/Relevant Links: 
- Optical Flow Implementation used by team: https://mpolinowski.github.io/docs/IoT-and-Machine-Learning/ML/2021-12-10--opencv-optical-flow-tracking/2021-12-10/
- https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html
- https://learnopencv.com/optical-flow-in-opencv/
- https://opencv24-python-tutorials.readthedocs.io/en/latest/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.html

Alternate Implementation of Stability: https://www.makeuseof.com/opencv-real-time-video-stabilization-how-to-implement/
