import cv2
import numpy as np
from processing import *


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('april21.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

prev_frame = []
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    # Add noise
    frame = saltAndPepperNoise(frame, 0.1)
    frame = gaussianNoise(frame)

    # Edge detection
    frame_edges = cv2.Canny(frame, 200, 200)

    # Shape description

    # Display the resulting frame
    cv2.imshow('Original Video', frame)
    cv2.imshow('Edges Video', frame_edges)

    # Keep previous frame
    prev_frame = frame

    # Press Q on keyboard to  exit
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

  # Break the loop
  else: 
    break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()