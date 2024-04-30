#threaded code iteration to acquire feed from two separate cameras in two separate threads, and stack the feed side-by-side
# import all required libraries as needed
import cv2
import time
import threading 
import numpy as np 
from siftVideo import Stitcher #import the stitcher class here
from vidgear.vidgear.gears.stabilizer import Stabilizer #import stabilizer here

from multiprocessing import Process, Pipe

# read from the first camera, and process frames as needed
def start_camera_1(chi_c, camera): 
    cam = cv2.VideoCapture(camera)
    while True: 
        ret, frame = cam.read()
        if ret: 
            chi_c.send(frame)

# read from the second camera, and process frames as needed
def start_camera_2(chi_c, camera): 
    cam = cv2.VideoCapture(camera)
    while True: 
        ret, frame = cam.read()
        if ret: 
            chi_c.send(frame)

# Apply the stabilizer onto both frames
def start_stream(): 
    # Initiate stabilizer here
    stab = Stabilizer(smoothing_radius=5,crop_n_zoom=True,border_size=8, logging=True)
    # create two piped threads for processing camera frames 1 and 2
    par_c_1, chi_c_1 = Pipe()
    par_c_2, chi_c_2 = Pipe()
    # initiate process for pipe 1
    process = Process(target=start_camera_1, args=(chi_c_1,1))
    process.start()

    #initiate process for pipe 2
    process = Process(target=start_camera_2, args=(chi_c_2,0))
    process.start()

    # while true, continue receiving frames, and process threads
    while True: 
        # receive frames for camera 1 and 2
        result_1 = par_c_1.recv()
        result_2 = par_c_2.recv()

        # Stack both results side by side
        frame = np.hstack((result_1,result_2))
        
        frame = cv2.resize(frame,(1280,500)) #resize based on need, 1280, 500 fits our needs in this case

        # Apply stabilizer onto conjoined frames
        frame = stab.stabilize(frame)
        # press q to exit the program if needed
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    # clean up all windows
    cv2.destroyAllWindows()

# call the function within main
if __name__ == '__main__':
    start_stream() 

    