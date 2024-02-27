import numpy as np
import cv2
import imutils

class Stitcher:
    def __init__(self):
        #added or_better in self.isv3 parameter
        self.isv3 = imutils.is_cv3(or_better=True) #determine if using latest openCV version and initialize cahced homography matrix
        self.cachedH = None

    def stitch(self, images, ratio=0.75, reprojThresh = 4.0, showMatches=False):
        #unpack images
        (imageB, imageA) = images
        (imageB, imageA) = images

        if self.cachedH is None:
            #find keypoints and extract
            (kpsA, featuresA) = self.detectAndDescribe(imageA)
            (kpsB, featuresB) = self.detectAndDescribe(imageB)

            #match features between images
            M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)

            #if no match then return nothing
            if M is None:
                return None
            
            #cache the homography matrix
            self.cachedH = M[1]
        #otherwise, apply a perspective warp to stich the image together
        #(matches, H, status) = M
            #    result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        result = cv2.warpPerspective(imageA, self.cachedH, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        imageB = cv2.resize(imageB, (result.shape[1], result.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        #check to see if the keypoint matches should be visualized
        #if showMatches: 
            #vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)

            #return a tuple of the sitched image and the visualization 
        #return (result, vis)
        
        #return the stitched image
        return result
                                     
                                     

        #apply perspective transform to stitch images together using homography matrix
        #result = cv2.warpPerspective(imageA, self.cachedH, (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))

        #result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        #return stitched image
        #return result
    def detectAndDescribe(self, image): 
        #convert the image to greyscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #check to see if we ae using OpenCV 3.X 
        if self.isv3: 
            #detect and extract features fom the image
            #descriptor = cv2.xfeatures2d.SIFT_create()
            #descriptor = cv2.xfeatures2d.SURF_create()
            #descriptor = cv2.SIFT()
            #print("PASSES THROUGH isv3 check")
            descriptor = cv2.SIFT_create()
            #print(descriptor)
            (kps, features) = descriptor.detectAndCompute(gray, None)
            #print("Printing out kps here: ")
            #print(kps)
            #print("Printing out features here: ")
            #print(features)
            #(kps, features) = descriptor.detectAndCompute(image, None)

        #otherwise we are using OpenCV 2.4.X: 
        else: 
            #detect keypoints in the image: 
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)

            #extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)

        #convert the keypoints from KeyPoint objects to Numpy arrays
        kps = np.float32([kp.pt for kp in kps])

        #return a tuple of keypoints anf features
        return (kps, features)
    
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # compute the raw matches and intialize the list of actual matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        #print("Raw Matches: ")
        #print(rawMatches)
        matches = []

        #loop over the raw matches
        print(len(rawMatches))
        for m in rawMatches: 
            # ensure th distance is within a certain ratio of each 
            # other (i.e. Lowe's ratio test)
            print("M0 Distance: ", m[0].distance)
            print("M1 Distance: ", m[1].distance * ratio)
            if (len(m) == 2) and m[0].distance < m[1].distance * ratio: 
                matches.append((m[0].trainIdx, m[0].queryIdx))
            print(matches)
            print(m)
            print("Before matches")
            #computing a homography requires at least 4 matches
            if (len(matches) > 4): 
                print("After matches")
                #construct the two sets of points
                ptsA = np.float32([kpsA[i] for (_, i) in matches])
                ptsB = np.float32([kpsB[i] for (i, _) in matches])

                #compute the homography between the two sets of points 
                (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)

                #return the matches along witht the homography matrix
                # and status of each matched point
                return (matches, H, status)
            
            #otherwise, no homography cou;d be computed
        return None
        
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status): 
        #initialize the output visualiation image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB

        #loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            #only process the match if the keypoint was successfully matches
            if s == 1: 
                #draw the match 
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

        #return the visualization 
        return vis





# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
#imageA = cv2.imread("image1.png", cv2.IMREAD_COLOR)
#imageA = imutils.resize(imageA, width=900)
#cv2.imshow("image",imageA)
#imageB = cv2.imread("image2.png",cv2.IMREAD_COLOR)
#imageB = imutils.resize(imageB, width=900)
#concatenate image Horizontally 
#Hori = np.concatenate((imageA, imageB), axis=1)

#Verti = np.concatenate((imageA, imageB), axis=0)

#cv2.imshow('Horizontal', Hori)
#cv2.imshow('Vertical',Verti)
"""
image = cv2.imread("image1.png")
aa = cv2.imread("image1.png",cv2.IMREAD_COLOR)
bb = cv2.imread("image2.png",cv2.IMREAD_COLOR)
cv2.imshow("frame1",aa)
cv2.imshow("frame2",bb)
"""

#cv2.imshow("image",imageB)
#ret1, frame1 = imageA
#ret2, frame2 = imageB
#frame = cv2.hconcat([frame1,frame2])
#cv2.imshow("frame",frame)
#imageB = cv2.imread(args["second"])
#imageA = imutils.resize(imageA,)
#imageB = imutils.resize(imageB, width=400)
#vid1 = cv2.VideoCapture(1) #Get Video feed from Camera 1
#vid2 = cv2.VideoCapture(2) #Get video feed from Camera 2

#ret1, frame1 = imageA
#ret2, frame2 = imageB
#frame = cv2.hconcat([frame1, frame2]) #Concatenates the two video feeds side by side

#cv2.imshow('frame', frame) #Displays the camera videos
#cv2.waitKey(0)
#cv2.destroyAllWindows()
"""while (True):
    ret1, frame1 = vid1.read() #reads the frames from Camera 1 
    ret2, frame2 = vid2.read() #reads the frames from Camera 2

    frame = cv2.hconcat([frame1, frame2]) #Concatenates the two video feeds side by side

    cv2.imshow('frame', frame) #Displays the camera videos

    if cv2.waitKey(1) & 0xFF == ord('q'): #If 'q' is pressed it will kill the programe
        break

vid1.release()
vid2.release()"""

#cv2.destroyAllWindows()
