import numpy as np
import scipy
import math
from scipy import stats
from skimage import measure
from skimage.morphology import convex_hull_image
import planktonator as plktor # delete - don't need it

def shape(img):
    '''
    width and height of object
    '''
    return np.shape(img)


def feret_diameter(x):
    
    # x: the binary image
    identity_convex_hull = convex_hull_image(x)
    coordinates = np.vstack(measure.find_contours(identity_convex_hull, 0.5, 
                                              fully_connected = 'high'))
    distances = scipy.spatial.distance.pdist(coordinates, 'sqeuclidean')
    return math.sqrt(np.max(distances))


def perimeter(mask,invert=False):
    '''
    Calculate total perimeter of all objects in binary image.
    calculates the perimeter of binary 2D shapes

    if background is white and the region of interest black,
    invert should be True.

    Parameters
    ----------
    mask : array_like
        binary image
    '''
    if invert:
        zeroidx     = mask == 0
        onesidx     = mask == 255
        maskinvert   = np.copy(mask)
        maskinvert[zeroidx] = 255
        maskinvert[onesidx] = 0
        return measure.perimeter(maskinvert > 110)
    else:
        return measure.perimeter(mask > 110)


def area(arr,bgwhite=True):
    '''
    Assumes background is white and region of interest
    is <255
    arr : array_like 
        contains pixel values in a 1D or 2D array
    '''
    if bgwhite:
        indicies = arr < 255
    else:
        indicies = arr > 0
    return np.sum(indicies)


def area_proportion(area,height,width):
    '''
        proportion of the image corresponding to the object
    '''    
    return (float(area)/(height*width))*100



def circularity(mask,area,perim=None,invert=False):
    '''
        circularity: 4pi(area/perim.^2)
    '''
    if perim == None:
        perim = perimeter(mask,invert=invert)

    return 4*np.pi*(area/np.power(perim,2))


def skelarea(mask,invert=False):
    '''
        skelarea: area of the one-pixel wide skeleton of the image
        background should be black and the object white
    '''
    from skimage.morphology import skeletonize
    masknorm        = np.divide(np.copy(mask),255)
    if invert:
        zeroidx     = masknorm == 0
        onesidx     = masknorm == 1
        masknorm[zeroidx] = 1
        masknorm[onesidx] = 0
        skeleton = skeletonize(masknorm)
    else:
        skeleton = skeletonize(masknorm)

    # plktor.image.io.save_image(np.multiply(skeleton,255),'skeleton.png')
    # sum of white skeleton pixels 
    return np.sum(skeleton==1)   

def feret():

    '''
        Maximum diameter

    '''
    return NotImplementedError


def intden(mean,area):
    '''
        intden: integrated density: mean*area
    '''
    return mean*area


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
    return np.median(arr)


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


def maxgrey(arr):
    '''
    max value
    '''
    return np.max(arr)


def mingrey(arr):
    '''
    min value
    '''
    return np.min(arr)


def rangegrey(arr):
    '''
        range: range of greys: max-min
    ''' 
    return maxgrey(arr)-mingrey(arr)


def meanpos(arr):
    '''
    meanpos: relative position of the mean grey: (max-mean)/range    
    '''
    return (np.max(arr) - np.mean(arr))/rangegrey(arr)


def coeffvar(arr):
    '''
    cv: coefficient of variation of greys: 100*(stddev/mean)
    '''
    return 100*(np.std(arr)/np.mean(arr))


def stdrange(arr):
    '''
    sr: index of variation of greys: 100*(stddev/range)
    '''
    return 100*(np.std(arr)/rangegrey(arr))


def perimmajor(perim,major):
    '''
    perimmajor: index of the relative complexity of the perimeter: perim/major
    '''
    return perim/major


def elongation(major,minor):
    '''
    elongation: elongation index: major/minor
    '''
    return major/minor


def majorminor(mask):
    '''
        length of major and minor axis of the best fitting ellipse
        Use the mask to determine max number of pixels in each dimension
        Assumes white background with black region of interest
    '''
    try:
        height, width = np.shape(mask)
    except:
        height, width, _ = np.shape(mask)

    maxlenj = 0
    for j in range(height):
        if np.divide(np.sum(mask[j,:]),255) > maxlenj: maxlenj = np.divide(np.sum(mask[j,:]),255)

    maxleni = 0
    for i in range(width):
        if np.divide(np.sum(mask[:,i]),255) > maxleni: maxleni = np.divide(np.sum(mask[:,i]),255)

    return max([int(maxlenj),int(maxleni)]),min([int(maxlenj),int(maxleni)]) 