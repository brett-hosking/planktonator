import numpy as np
from scipy import stats

def shape(img):
    '''
    width and height of object
    '''
    return np.shape(img)


def area(arr):
    '''
    area of object in image given contour

    arr : array_like 
        contains pixel values in a 1D or 2D array
    '''
    return len(arr)


def mean(arr):
    '''
    Mean intensity

    arr : array_like 
        contains pixel values in a 1D or 2D array
    '''
    return np.mean(arr)


def median(arr):
    '''
    Median intensity
    '''
    raise NotImplementedError


def std(arr):
    '''
    Standard deviation of intensity values
    '''
    return np.std(arr)


def mode(arr):
    '''
    Mode of intensity values
    '''
    return stats.mode(arr)[0][0]


def max(arr):
    '''
    max value
    '''
    return np.max(arr)


def min(arr):
    '''
    min value
    '''
    return np.min(arr)