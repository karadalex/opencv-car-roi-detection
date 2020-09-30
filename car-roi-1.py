import cv2
import numpy as np
from processing import *
from algorithms import algorithm1
import time


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('april21.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

prev_frame_time = time.time()
fps_list = []

prev_frame = []
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    roi_mask, masked_frame = algorithm1(frame)

    # Display the resulting frame
    cv2.imshow('Original Video', frame)
    cv2.imshow('ROI Mask', roi_mask*255)
    cv2.imshow('ROI Video', masked_frame)

    # Keep previous frame
    prev_frame = frame

    # Calculate fps metric
    current_frame_time = time.time()
    seconds = current_frame_time - prev_frame_time
    prev_frame_time = current_frame_time
    fps = round(1/seconds, 2)
    fps_list.append(fps)

    # Press S on keyboard to save images
    key = cv2.waitKey(25)
    if key == ord('s'):
      cv2.imwrite('original1.png', frame)
      cv2.imwrite('roi-mask1.png', roi_mask*255)
      cv2.imwrite('masked_frame1.png', masked_frame)
    # Press Q on keyboard to  exit
    if key == ord('q'):
      break

  # Break the loop
  else: 
    break

# Calculate total fps statistics
fps_list = np.array(fps_list)
fps_avg = np.average(fps_list)
fps_std = np.std(fps_list)
print("FPS average: ", fps_avg)
print("FPS standard deviation: ", fps_std)

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()