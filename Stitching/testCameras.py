import cv2

# file verifies, which camera is currently in position
def find_available_cameras(limit=10):
    """
    Attempts to open video capture devices up to a specified limit.
    Prints out the indexes of available cameras.

    :param limit: The upper limit for camera indexes to test.
    """
    available_cameras = []
    for i in range(limit): # iterate through the number of  devices captured
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) # cv2.CAP_DSHOW is added for Windows compatibility
        if cap.isOpened(): # if video capture is open
            print(f"Camera found at index: {i}") # print out camera at specific device
            available_cameras.append(i) # append to the number of available cameras
            cap.release() # release the video capture
        else:
            print(f"No camera found at index: {i}") # if no device detected, print the following
    
    return available_cameras # return number of cameras found

# Adjust the limit if you expect more cameras to be connected
available_cameras = find_available_cameras(limit=10)
print("Available Cameras:", available_cameras)
