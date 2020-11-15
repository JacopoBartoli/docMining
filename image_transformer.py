import numpy as np
import cv2


def image_transformation(img):
    # Transform the image utilizing distance transform.
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Check if the threshold is right. (254)
    (thresh, bn_img) = cv2.threshold(gray_img, 254, 255, cv2.THRESH_BINARY)

    # The metric used for distance is euclidean
    blue_channel = cv2.distanceTransform(bn_img, distanceType=cv2.DIST_L2, maskSize=5)
    # Linear distance transform. This is L1 norm. I suppose this is the right distance
    green_channel = cv2.distanceTransform(bn_img, distanceType=cv2.DIST_L1, maskSize=3)
    # Max distance transform. max(|x1-x2|,|y1-y2|)
    red_channel = cv2.distanceTransform(bn_img, distanceType=cv2.DIST_C, maskSize=3)

    # Merge the three channel
    transformed = cv2.merge((blue_channel, green_channel, red_channel))
    # Make the image in gray scale again.
    transformed = cv2.cvtColor(transformed, cv2.COLOR_BGR2GRAY)
    # Convert the image in the right format. Only if adaptive threshold is used.
    # transformed = np.uint8(transformed)

    # The first value of the threshold should be adapted.
    # We can try to use cv2.THRESH_OTSU. Need to read documentation first
    ret, transformed = cv2.threshold(transformed, 15, 255, cv2.THRESH_BINARY)

    # Adaptive threshold seems to not be the right answer at this threshold problem.
    # transformed = cv2.adaptiveThreshold(transformed, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 0)

    return transformed


if __name__ == '__main__':
    print("void")
