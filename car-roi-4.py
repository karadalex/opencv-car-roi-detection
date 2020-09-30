import cv2
import numpy as np
from processing import *
from algorithms import algorithm2


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
    original_frame = np.copy(frame)

    # Add noise
    frame = saltAndPepperNoise(frame, 0.01)
    frame = gaussianNoise(frame, 400)

    # Apply 1st algorithm to noisy frame
    masked_frame, roi_mask, roi_mask1, roi_mask2, roi_mask3 = algorithm2(frame)

    # Display the resulting frame
    cv2.imshow('Original Video', original_frame)
    cv2.imshow('Noisy Video', frame)
    cv2.imshow('ROI Mask', roi_mask*255)
    cv2.imshow('ROI Video', masked_frame)

    # Keep previous frame
    prev_frame = frame

    # Press S on keyboard to save images
    key = cv2.waitKey(25)
    if key == ord('s'):
      cv2.imwrite('original4.png', original_frame)
      cv2.imwrite('noisy4.png', frame)
      cv2.imwrite('roi-mask4-1.png', roi_mask1*255)
      cv2.imwrite('roi-mask4-2.png', roi_mask2*255)
      cv2.imwrite('roi-mask4-3.png', roi_mask3*255)
      cv2.imwrite('roi-mask4.png', roi_mask*255)
      cv2.imwrite('masked_frame4.png', masked_frame)
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