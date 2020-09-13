import numpy as np
import cv2
import random
import math
from helpers import *


def blurring(image, radius=2):
    """[summary]

    Args:
        image ([type]): [description]
        radius (int, optional): [description]. Defaults to 2.

    Returns:
        [type]: [description]
    """
    filter = np.ones((5,5), np.float32)/25
    filtered_img = cv2.filter2D(image, -1, filter)
    return filtered_img


def medianFilter(image, radius=2):
    """[summary]

    Args:
        image ([type]): [description]
        radius (int, optional): [description]. Defaults to 2.
    """
    pass


def saltAndPepperNoise(image, percentage):
    """[summary]

    Args:
        image (opencv image): Original image to add noise to
        percentage (float): From 0 to 1, percentage of pixels that have noise

    Returns:
        [type]: [description]
    """
    # Get size of image
    (rows, cols, _) = image.shape
    pixels_num = rows*cols

    for p in range(int(percentage*pixels_num)):
        i = random.randint(0, rows-1)
        j = random.randint(0, cols-1)
        
        noiseVal = random.choice([0, 255])
        image[i,j] = noiseVal
            
    return image


def gaussianNoise(image, power=1):
    """[summary]

    Args:
        image ([type]): [description]
        power (int, optional): [description]. Defaults to 1.

    Returns:
        [type]: [description]
    """
    noise = np.zeros(image.shape).astype(np.uint8)
    mean = 0
    sigma = math.sqrt(power)
    cv2.randn(noise, mean, (sigma, sigma, sigma))
    image = cv2.add(image, noise)
    return image