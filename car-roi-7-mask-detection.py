import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from drawnow import drawnow, figure
from processing import *
from algorithms import algorithm2


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('april21.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Apply ROI detection algorithm
    masked_frame, roi_mask, roi_mask1, roi_mask2, roi_mask3 = algorithm2(frame, lower_threshold=115, upper_threshold=135)
    
    shadow_threshold = 10
    masked_gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
    shadows = (masked_gray < shadow_threshold).astype(np.uint8)
    # Dilate shadows (morphological operator) so that we can easier mu
    dilation_kernel = np.ones((4,4),np.uint8)
    dilated_shadows = cv2.dilate(shadows, dilation_kernel, iterations = 1)

    # Edge detection on masked frame
    frame_edges = cv2.Canny(masked_frame, 200, 200)

    # Display the resulting frame
    cv2.imshow('Original Video', frame)
    cv2.imshow('ROI Mask', roi_mask*255)
    cv2.imshow('ROI Video', masked_frame)
    cv2.imshow('Shadows', shadows*255)
    cv2.imshow('Dilated Shadows', dilated_shadows*255)
    car_mask = frame_edges*dilated_shadows
    cv2.imshow('Car mask', car_mask)

    # Keep previous frame
    prev_frame = frame

    # Press S on keyboard to save images
    key = cv2.waitKey(25)
    if key == ord('s'):
      cv2.imwrite('roi-mask7.png', roi_mask*255)
      cv2.imwrite('masked_frame7.png', masked_frame)
      cv2.imwrite('shadows7.png', shadows*255)
      cv2.imwrite('dilated_shadows7.png', dilated_shadows*255)
      cv2.imwrite('frame_edges.png', frame_edges)
      cv2.imwrite('car-mask.png', car_mask)
    # Press Q on keyboard to  exit
    if key == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()