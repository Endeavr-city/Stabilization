# import required libraries
from vidgear.gears import VideoGear
import numpy as np
import cv2

# open any valid video stream with stabilization enabled(`stabilize = True`)
stream_stab = VideoGear(source="ShakyVideos/shaky_video_2.mp4", stabilize=True).start()

# loop over
while True:

    # read stabilized frames
    frame_stab = stream_stab.read()

    # check for stabilized frame if None-type
    if frame_stab is None:
        break

    # {do something with the frame here}

    # Show output window
    cv2.imshow("Stabilized Output", frame_stab)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close streams
stream_stab.stop()
