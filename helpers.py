import numpy as np


def linearMap(x, min1, max1, min2, max2):
    """CHange range of x from range [min1, max1] to [min2, max2]

    Args:
        x ([ndarray, any]): [description]
        min1 ([any]): [description]
        max1 ([any]): [description]
        min2 ([any]): [description]
        max2 ([any]): [description]

    Returns:
        [any]: Value from new range
    """
    range1 = max1 - min1
    range2 = max2 - min2
    y = (x - min1)*range2/range1 + min2
    return y