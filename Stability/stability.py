#Import numpy and cv2 
import numpy as np
import cv2
from imutils.video import VideoStream

#Function returns a smooth curvem and helps to reduce noise and fluctuations in the cuvre. 
#Does this by averaging the values within the sliding window
def calculate_moving_average(curve, radius): 
  #Calculate the moving aerage of a curve using a given radius 
  window_size = 2 * radius + 1
  kernel = np.ones(window_size)/window_size 
  curve_padded = np.lib.pad(curve, (radius, radius), 'edge')
  smoothed_curve = np.convolve(curve_padded, kernel, mode='same')
  smoothed_curve = smoothed_curve[radius:-radius]
  return smoothed_curve

#applies moving average on each dimension of trajectory by creating a smoothed copy of the original trajectory
def smooth_trajectory(trajectory):
	#smooth trajectory using moving average on each dimension
  smoothed_trajectory = np.copy(trajectory)
  
  for i in range(3):
    smoothed_trajectory[:,i] = calculate_moving_average(
       trajectory[:,i], 
       radius=SMOOTHING_RADIUS)
    
  return smoothed_trajectory
  
#fixes the brder of frame by applying rotation and scaling formation
#takes an input frame, calculates its shape, constructs transformation matrix and applies transformation to frame
def fix_border(frame):
  frame_shape = frame.shape
  matrix = cv2.getRotationMatrix2D(
    (frame_shape[1] / 2, frame_shape[0] / 2),
    0,
    1.04
  )
  frame = cv2.warpAffine(frame, matrix, (frame_shape[1], frame_shape[0]))
  return frame
                                  
#Initializaing video stabilization and taking the input 
SMOOTHING_RADIUS = 50 
#pass in the video path of the shaky video, in this case the video stream of our stitched video 
#Open the input video file
#Replace the path with 0 to use your webcam
# cap = cv2.VideoCapture(0) #set to 2, since we would want to retrieve the camera according to the Orin's specification
# #cap = VideoStream(src=1).start()
# if (cap.isOpened):
#    print("Camera is OPENED")
# else: 
#    print("Camra is NOT OPEN")
#cap = cv2.VideoCapture("highway_day_2024-02-08_12-39-04-front.mp4") - Tesla Video
cap = cv2.VideoCapture("ShakyVideos/shaky_video.mp4") # Attached camera feed

#shaky video properties
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS) #get frame rate per second
# apply the correct video format, for video output
fourcc = cv2.VideoWriter_fourcc(*'mp4v') #convert output to mp4
out = cv2.VideoWriter('StabilizedOutput/stabilized_video.mp4',
                      fourcc, 
                      fps, 
                      (2 * width, int(height))) #process new video with provided specs and fps
                       
#Reading and Processing Frames
_, prev_frame = cap.read()
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

print("Num Frames: ", num_frames)
transforms = np.zeros((num_frames - 1, 3), np.float32)

#Calculate optical flow between consecutive frames
#Estimate affine transformation between points
for i in range(num_frames - 2):
    #prev_points = cv2.goodFeaturestoTrack(prev_gray, maxCorners=200, qualityLevel=0.01, minDistance=30, blockSize=3)
    # track all good features from the grayscaled image
    prev_points = cv2.goodFeaturesToTrack(
      prev_gray, 
      maxCorners=200,
      qualityLevel=0.01,
      minDistance=30,
      blockSize=3
    )
    # read the current frames successively
    success, curr_frame = cap.read()
    # error-check if frame-reading fails
    if not success:
        break
    # convert the current frame to gray-scale
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
  
    # apply the cv2 optical flow line onto the previous grayscale image, and the current greyscale image frame
    curr_points, status, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_points, None)
  
    # verify and check that the shape of the previous and the current frames are the same
    assert prev_points.shape == curr_points.shape
    idx = np.where(status ==1)[0]
    prev_points = prev_points[idx]
    curr_points = curr_points[idx]
  
  #Estimate affine transformation between points
    matrix, _ = cv2.estimateAffine2D(prev_points, curr_points)
    translation_x = matrix[0,2]
    translation_y = matrix[1,2]
    rotation_angle = np.arctan2(matrix[1,0], matrix[0,0])
    transforms[i] = [translation_x, translation_y, rotation_angle]
    prev_gray = curr_gray
  
  
#smoothing the trajectory
trajectory = np.cumsum(transforms, axis=0)
smoothed_trajectory = smooth_trajectory(trajectory)
difference = smoothed_trajectory - trajectory
transforms_smooth = transforms + difference
  
  
  
#Stabilizing and Writing Frames 
#Start by resetting the video capture. This ensures future operations will read from the start of the video.
cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


#Then, stabilize the video by processing each frame 
#Process each frame and stabilize the video 
for i in range(num_frames - 2): 
    # capture each frame in a loop
    success, frame = cap.read()
    # if not successful, break as needed
    if not success:
        break 
    
    translation_x = transforms_smooth[i, 0]
    translation_y = transforms_smooth[i, 1]
    rotation_angle = transforms_smooth[i, 2]

    #Create the transformation matrix for stabilization 
    transformation_matrix = np.zeros((2,3), np.float32)
    transformation_matrix[0,0] = np.cos(rotation_angle)
    transformation_matrix[0, 1] = -np.sin(rotation_angle)
    transformation_matrix[1,0] = np.sin(rotation_angle)
    transformation_matrix[1,1] = np.cos(rotation_angle)
    transformation_matrix[0,2] = translation_x 
    transformation_matrix[1,2] = translation_y

    #Apply the transformation to stabilize the frame 
    frame_stabilized = cv2.warpAffine(frame, transformation_matrix, (width, height))
    #Fix the border of the stabilized frame
    frame_stablized = fix_border(frame_stabilized)
    #Concatenate the original and stabilized frames side by side
    frame_out = cv2.hconcat([frame, frame_stablized])
    # Resize the frame if its width exceeds 1920 pixels
    if frame_out.shape[1] > 1920:
        frame_out = cv2.resize(
        frame_out,
        (frame_out.shape[1], frame_out.shape[0])
        )
    #display the before and after frames
    #cv2.imshow("Before and after", frame_out[0])
    cv2.imshow('frame_out',frame_out) #Derived from 1st commit, display original frame and trained_frame side by side
    cv2.waitKey(10)
    #write the frame to the output video file
    out.write(frame_out) # required for writing all frames to output video, so that the final video is not corrupted
      

# Release the video capture and writer, and close any open windows
cap.release()
out.release() #Added line back so as to release output correctly for stabilized video
cv2.destroyAllWindows()
    
  
  
  
  