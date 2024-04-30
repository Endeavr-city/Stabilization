import numpy as np
import cv2
import imutils

# Stitcher class
class Stitcher:
    def __init__(self):
        # Initialization remains the same; adjustments for ORB are not needed here
        self.isv3 = imutils.is_cv3(or_better=True)
        self.cachedH = None

    # function to stitch both images, with an appropriate ratio and reprojection-threshold
    def stitch(self, images, ratio=0.75, reprojThresh=4.0, showMatches=False):
        # Stitching process logic remains largely the same
        (imageB, imageA) = images #store both images as an object
        # if homography matrix is none
        if self.cachedH is None:
            # detect and describe key features on image A and image B
            (kpsA, featuresA) = self.detectAndDescribe(imageA)
            (kpsB, featuresB) = self.detectAndDescribe(imageB)
            
            # match keypoints between features on both images, and store in a matrix
            M = self.matchKeypoints(kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh)
            # if matrix is none, do an error-check and return accordingly
            if M is None:
                return None
            # assign cached matrix to first element of the stored matrix
            self.cachedH = M[1]
        # Apply warp-perspective to overlapt the second image onto the first image, ie, right frame onto left frame
        result = cv2.warpPerspective(imageA, self.cachedH,
                                     (imageA.shape[1] + imageB.shape[1], imageA.shape[0]))
        result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        # return result
        return result

    # detect and describe key features from an image
    def detectAndDescribe(self, image):
        # convert the image to grey-scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # handle for a special-case, with detet and compute image applied here
        if self.isv3:
            descriptor = cv2.ORB_create()
            (kps, features) = descriptor.detectAndCompute(image, None)
        else:
			# detect keypoints in the image
            detector = cv2.FeatureDetector_create("ORB")
            kps = detector.detect(gray)
			# extract features from the image
            extractor = cv2.DescriptorExtractor_create("ORB")
            (kps, features) = extractor.compute(gray, kps)
		# convert the keypoints from KeyPoint objects to NumPy
		# arrays
        kps = np.float32([kp.pt for kp in kps])
		# return a tuple of keypoints and features
        return (kps, features)

    # match keypoints between features from two images
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB, ratio, reprojThresh):
        # The matching process does not need to be changed for ORB; it works with both binary and float descriptors.
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
        # match keypoints, using the knn match functionality
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        # create an empty matches matrix for computations
        matches = []
        # Apply the appropriate raw-matches as per the formula, and store in matrix as needed
        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        # check if the number of matches is greater than 4
        if len(matches) > 4:
            # extract matches points from the keypoints of imageA, and do the same for imageB
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])
            # find the homographt matrix, from the keypoints of image A and image B
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, reprojThresh)
            # return appropriate number of matches, with the correct homography matrix
            return (matches, H, status)
        # Else, return none
        return None

    # draw matches between features of image A and B
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