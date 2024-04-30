# import required libraries
from vidgear.vidgear.gears.stabilizer import Stabilizer
from vidgear.vidgear.gears import CamGear
from vidgear.vidgear.gears import WriteGear
import cv2

# To open live video stream on webcam at first index(i.e. 0) device
stream = CamGear(source=0, logging=True).start()

output_params = {"-output_dimensions": (1280, 720)} #third method, by directly modifying frame-rate with length and width of camera frame

# Define writer with defined parameters and suitable output filename, use VidGear WriteGear to process this
writer = WriteGear(output="C:/Users/asahu/OneDrive/Desktop/TAMUDocs-WindowsCopy/TAMUDocsSeniorYear/CapstoneFiles/Stabilization/StabilizedOutput/frameTest1.mp4", logging = True, **output_params)

# initiate stabilizer object with defined parameters
# first testing done using 10 frames
# second testing done using 20 frames
# third testing done using 5 frames
stab = Stabilizer(smoothing_radius=5, crop_n_zoom=True, border_size=8, logging=True)

# loop over
while True:

    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # send current frame to stabilizer for processing
    stabilized_frame = stab.stabilize(frame)

    # wait for stabilizer which still be initializing
    if stabilized_frame is None:
        continue

    # {do something with the stabilized frame here}
    # for testing purposes, we want to output the old frame and the newly stabilized frame side by side
    output_frame = cv2.hconcat([frame, stabilized_frame])

    #writer frame to writer, also used in compression method
    writer.write(output_frame) #Extract the output frame, and write to the mp4

    #Show the combined output window, showing original video and stabilized video side by side
    cv2.imshow('output_frame', output_frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# clear stabilizer resources
stab.clean()

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()

# safely close the writer 
writer.close()