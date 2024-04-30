import numpy as np
import cv2
import imutils
#from skimage import transform
#from skimage import filters

class Stitcher:
    def __init__(self):
        #added or_better in self.isv3 parameter
        self.isv3 = imutils.is_cv3(or_better=True) #determine if using latest openCV version and initialize cahced homography matrix
        self.cachedH = None

    # feature that stitches both frames side-by-side, apply a best-fitting ratio and reprojection-threshold as needed
    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        (imageB, imageA) = images #store both images A and B as an object
        # if no homography matrix is detected
        if self.cachedH is None:
            # detect and describe key features from image A, and do the same for image B
            (kpsA, featuresA) = self.detectAndDescribe(imageA)
            (kpsB, featuresB) = self.detectAndDescribe(imageB)
            
            # get matched keypoints from the features extracted by both images, and store in a matrix
            M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)
            # if matrix is none, error-check here
            if M is None:
                return None
            
            #self.cachedH = M[1]
            (matches, self.cachedH, status) = M

        # Apply the warp-perspective function onto both images, to properly overlay the second frame onto the first frame, ie right frame onto left frame
        result = cv2.warpPerspective(imageA, self.cachedH,
                                 (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB

        # Crop the result to the largest rectangular area
        result = self.crop_to_largest_rectangle(result)

        # draw matches between image A and B, along with key features
        if showMatches:
            vis  = self.drawMatches(imageA, imageB, kpsA, kpsB, matches, status)
            return (result, vis)
        # return result
        return result

    # for the stitched image, crop to get the largest conjoined rectangle area, so that the view is properly output
    def crop_to_largest_rectangle(self, image):
        # Convert the image to grayscale and then binary image
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour area and its bounding rectangle
        largest_area = 0
        best_rect = (0, 0, 0, 0)  # x, y, width, height
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            area = w * h
            if area > largest_area:
                largest_area = area
                best_rect = (x, y, w, h)

        # Crop the image to the bounding rectangle of the largest contour
        if largest_area > 0:
            x, y, w, h = best_rect
            cropped_image = image[y:y+h, x:x+w]
            return cropped_image
        else:
            return image  # Return original if no contours found

    # detect and describe all key features from a specific image    
    def detectAndDescribe(self, image):
        # convert image to gray-scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # special-case for applying detect and compute
        if self.isv3:
            descriptor = cv2.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)
        else:
			# detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)
			# extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)
		# convert the keypoints from KeyPoint objects to NumPy
		# arrays
        kps = np.float32([kp.pt for kp in kps])
		# return a tuple of keypoints and features
        return (kps, features)
    
    # match the keypoints between the features of two separate images
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
		ratio, reprojThresh):
        #matcher = cv2.DescriptorMatcher_create("BruteForce")
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_FLANNBASED)
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
		# loop over the raw matches
        for m in rawMatches:
			# ensure the distance is within a certain ratio of each
			# other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        #computing a homography requires at least 4 matches
        if (len(matches) > 4): 
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
        
    # draw matches between key features of both images
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status): 
        #initialize the output visualiation image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
		# loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
			# only process the match if the keypoint was successfully
			# matched
            if s == 1:
				# draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)

        #return the visualization 
        return vis
 
