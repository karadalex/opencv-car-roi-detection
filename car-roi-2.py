import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from drawnow import drawnow, figure
from processing import *
from algorithms import algorithm2
import time


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


def draw_fig():
  global frame, gray, hist
  if frame.any():
    # convert to grayscale
    # TODO: this needs to be replaced, because it is calculated twice in every frame!
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # show the plotting graph of an image 
    hist = plt.hist(gray.ravel(), 256, [0,256], density=True)
    plt.title('Histogram')
    plt.show()


prev_frame_time = time.time()
fps_list = []
# Read until video is completed
while(cap.isOpened()):
  # Capture frame-by-frame
  ret, frame = cap.read()
  if ret == True:
    # Calculate histogram and plot it: comment this line when measuring fps
    # drawnow(draw_fig)

    # Apply ROI detection algorithm
    masked_frame, roi_mask, roi_mask1, roi_mask2, roi_mask3 = algorithm2(frame)

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