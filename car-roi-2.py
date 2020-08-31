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
lower_threshold = 115
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
    roi_mask = roi_mask1 * roi_mask2 * 255
    print(roi_mask)

    # Apply ROI mask to frame
    
    # Step 2: Edge detection
    frame_edges = cv2.Canny(frame, 200, 200)

    # Step 3: Shape description

    # Display the resulting frame
    cv2.imshow('Original Video', frame)
    cv2.imshow('Edges Video', frame_edges)
    cv2.imshow('ROI Mask', roi_mask)

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