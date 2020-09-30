from processing import *


def algorithm1(frame, topY=None, bottomY=None):
  """[summary]

  Args:
      frame ([type]): [description]
      topY ([type], optional): [description]. Defaults to None.
      bottomY ([type], optional): [description]. Defaults to None.

  Returns:
      [type]: roi_mask, masked_frame
  """
  roi_mask = np.zeros(frame.shape[0:2])

  if not topY:
    topY = int(3*frame.shape[0]/5)
  if not bottomY:
    bottomY = frame.shape[0]
  
  roi_mask[topY:bottomY, :] = 1
  roi_mask = roi_mask.astype(np.uint8)

  # Apply mask
  masked_frame = applyMaskToFrame(frame, roi_mask)

  return roi_mask, masked_frame


def algorithm2(frame, lower_threshold=120, upper_threshold=130):
  """[summary]

  Args:
      frame ([type]): [description]
      lower_threshold (int, optional): Lower threshold for histogram. Defaults to 120.
      upper_threshold (int, optional): Upper threshold for histogram. Defaults to 130.

  Returns:
      [type]: masked_frame, roi_mask, roi_mask1, roi_mask2, roi_mask3
  """
  # convert to grayscale
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

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

  return masked_frame, roi_mask, roi_mask1, roi_mask2, roi_mask3