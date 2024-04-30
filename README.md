# RetroPilot: Stitching, Stabilization and Object Segmentation

The central code repository for this project is split into three distinct folders, each of which contains code for the three major integrations of this project: Video Stitching, Video Stabilization and Object Segmentation. 

For this specific project, the VidGear open-source library was used extensively to stabilize the video feed during the video stabilization phase. Details on downloading and importing the VidGear library as needed are present at the following link: https://abhitronix.github.io/vidgear/v0.3.2-stable/. 
VidGear GitHub: https://github.com/abhiTronix/vidgear. 

The object segmentation portion of this project, utilized the YoloV8 machine-learning model to train and segment objects. Official Link to YoloV8 documentation: https://docs.ultralytics.com.
YoloV8 github: https://github.com/ultralytics/ultralytics.


As an overview, the three main aspects of this project are described below: 
1. Video Stitching: This feature provides the ability for two videos to be able to stitch together into one conjoined frame. In an ideal case, the user would be able to extract two video feeds by capturing image frames from two cameras which are conjoined side by side in one view frame. Both cameras need to detect a frontal uniform view of the images in front of them, with a slight angular tilt and adjustability, as needed. The main idea here is that the algorithm will be able to detect key feature points from both images, by first converting both images into greyscale. 

Once the key feature points are detected from both images, the cameras would be able to draw matches between specific key points from the features. Here, a specific threshold is applied, which filters out certain features, that fall beneath the threshold values in terms of greyscaling. The algorithm would be able to draw matches between certain feature points, and then output the data appropriately into a matrix format. Essentially, the matrix format is the culmination of common feature points between both cameras, which is used to create a commonly conjoined video feed. Lastly, we overlay the image feed from the second camera, ie the right camera onto the image feed of the left camera. For further documentation, please refer to the following documentation: https://pyimagesearch.com/2016/01/25/real-time-panorama-and-image-stitching-with-opencv/.

2. Video Stabilization: The main idea here is that for whatever video feed the user is able to obtain from either one camera, or two cameras, if the feed is concatenated or stitched together, the video feed should be stable in most conditions. Regardless of how smooth or rough the path of the road is, the video feed should be stable during most times. For this portion, the team relied on the video stabilization references provided by the VidGear open source library. For additional references, please refer to official vidGear documentation. 

Important/Relevant VidGear Links: 
https://abhitronix.github.io/vidgear/latest/gears/stabilizer/usage/#using-videogear-with-stabilizer-backend
https://abhitronix.github.io/vidgear/latest/gears/stabilizer/params/#crop_n_zoom
https://abhitronix.github.io/vidgear/latest/switch_from_cv/#switching-videocapture-apis
https://abhitronix.github.io/vidgear/latest/gears/videogear/usage/#bonus-examples
https://github.com/abhiTronix/vidgear?tab=readme-ov-file

3. Object Segmentation: During the drive time of a vehicle, the algorithm will be able to utilize either feed from one camera/video, or two cameras accordingly, and segment specific objects it encounters along the path. It creates a bounding shape around specific objects, and classifies them appropriately, whether its a car, road sign, pedestrian, or road pavement etc. The team utilized over 6000 images to train the YoloV8 segmentation model on common road objects, such as a car, pedestrian and road signs. For further references, refer to the official YoloV8 documentation: https://docs.ultralytics.com. 

Official Ultralytics GitHub: https://github.com/ultralytics/ultralytics. 
