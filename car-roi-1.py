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

    # Create ROI mask
    roi_mask = np.zeros(frame.shape[0:2])
    roi_mask[int(3*frame.shape[0]/5):frame.shape[0], :] = np.ones((frame.shape[0]-int(3*frame.shape[0]/5), frame.shape[1]))
    roi_mask = roi_mask.astype(np.uint8)

    # Step 1: Frame processing/improvement
    frame = blurring(frame)

    # Apply mask
    masked_frame = np.zeros(frame.shape).astype(np.uint8)
    for c in range(frame.shape[2]):
      masked_frame[:,:,c] = frame[:,:,c] * roi_mask

    # Step 2: Edge detection
    frame_edges = cv2.Canny(masked_frame, 200, 200)

    # Step 3: Shape description

    # Display the resulting frame
    cv2.imshow('Original Video', frame)
    cv2.imshow('ROI Mask', roi_mask*255)
    cv2.imshow('ROI Video', masked_frame)
    # cv2.imshow('Edges Video', frame_edges)

    # Keep previous frame
    prev_frame = frame

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

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()