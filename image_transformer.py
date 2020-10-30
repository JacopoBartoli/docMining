import numpy as np
import cv2
from scipy.ndimage import distance_transform_edt


def image_transformation(img):
    # Transform the image utilizing distance transform.

    # The metric used for distance is euclidean
    blue_channel = distance_transform_edt(img)
    # Linear distance transform !!!
    green_channel = None
    # Max distance transform
    red_channel = None
    transformed = cv2.merge((blue_channel, green_channel, red_channel))
