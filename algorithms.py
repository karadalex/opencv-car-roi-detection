from processing import *


def algorithm1(frame, topY=None, bottomY=None):
  """[summary]

  Args:
      frame ([type]): [description]
      topY ([type], optional): [description]. Defaults to None.
      bottomY ([type], optional): [description]. Defaults to None.

  Returns:
      [type]: [description]
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