# ROI calculation

ROI recalculation every 10 frames (set it as parameter)

## 1st solution

ignore constant scenes (sky):
- ignore upper half frame (slow changes)
- heep lower half frame (faster changes)


## 2nd solution

road is gray:
- Use gray levels histogram => live plot with matplotlib
- Histogram equation

Compare solutions with fps


# Car detection

- next car postion will be near (spatial & temporal locality)
- Chain descriptors


# Programs index

1. ROI Algorithm 1
2. ROI Algorithm 2
3. Noise + ROI Algorithm 1
4. Noise + ROI Algorithm 2
5. Noise Reduction + ROI Algorithm 1
6. Noise Reduction + ROI Algorithm 2
7. Car Detection mask