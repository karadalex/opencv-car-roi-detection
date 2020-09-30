import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from drawnow import drawnow, figure
from processing import *


# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('april21.avi')

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")

fig = plt.figure()
plt.ion() #Tell matplotlib you want interactive mode to plot live data

# Initialize global variables
prev_frame = []
frame = []
gray = []
hist = []
roi_mask = []

# ROI parameters:
# Histogram thresholds
lower_threshold = 120
upper_threshold = 130

def draw_fig():
  global frame, gray, hist
  if frame.any():
    # convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show the plotting graph of an image 
    hist = plt.hist(gray.ravel(), 256, [0,256], density=True)
    plt.title('Histogram')
    plt.show()


# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:

    drawnow(draw_fig)
    # Step 1: Frame processing/improvement
    # frame = blurring(frame)

    # Calculate ROI mask
    roi_mask1 = (gray > lower_threshold).astype(np.uint8)
    roi_mask2 = (gray < upper_threshold).astype(np.uint8)
    roi_mask3 = roi_mask1 * roi_mask2
    # Sum number of white pixels per row
    white_pixels = np.sum(roi_mask3, axis=1)
    rowNum = len(white_pixels)
    # Scan roi_mask3 top-to-bottom and bottom-to-top to get the roi
    topY = 0
    bottomY = rowNum-1
    for i in range(rowNum):
      if white_pixels[i] >= 60:
        topY = i
        break
    for i in reversed(range(rowNum)):
      if white_pixels[i] >= 60:
        bottomY = i
        break
    roi_mask = np.zeros(roi_mask3.shape).astype(np.uint8)
    roi_mask[topY:bottomY, :] = 1

    # Apply ROI mask to frame
    masked_frame = np.zeros(frame.shape).astype(np.uint8)
    for c in range(frame.shape[2]):
      masked_frame[:,:,c] = frame[:,:,c] * roi_mask
    
    # Step 2: Edge detection
    frame_edges = cv2.Canny(frame, 200, 200)

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
      cv2.imwrite('original2.png', frame)
      cv2.imwrite('roi-mask2-1.png', roi_mask1*255)
      cv2.imwrite('roi-mask2-2.png', roi_mask2*255)
      cv2.imwrite('roi-mask2-3.png', roi_mask3*255)
      cv2.imwrite('roi-mask2.png', roi_mask*255)
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