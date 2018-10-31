from skimage import measure
import scipy.ndimage as ndimage 
import numpy as np
import planktonator as plktor

def threshold(img,t=240):
    '''
    Create a mask of objects by applying a pixel threshold

    Parameters
    ----------
    arr : array_like
        2D image array, uint8
    t : int 
        pixel threshold

    Returns
    -------
    object image mask
    '''
    mask            = np.array(np.zeros(np.shape(img)))
    highidx         = img>=t
    lowidx          = img<t
    mask[highidx]   = 255
    mask[lowidx]    = 0
    return mask


def convolution(img,kernel):
    return ndimage.convolve(img,kernel)

def find_contours(mask):
    '''
        Use skimage to find contours in image mask
    '''
    return measure.find_contours(mask, 0)


def removescale(img, a=[1200,1230,0,500], p=255):
    '''
        Remove the scale bar from image
    '''
    img[a[0]:a[1],a[2]:a[3]] = p
    return img

def maskfill(mask,contours):
    '''
        Ensure that any gaps in blobs are filled within the mask

    '''
    # Create an empty image to store the masked array
    r_mask = np.zeros_like(mask, dtype='bool')

    for contour in contours:
        # Create a contour image by using the contour coordinates rounded to their nearest integer value
        r_mask[np.round(contour[:, 0]).astype('int'), np.round(contour[:, 1]).astype('int')] = 1

    # Fill in the hole created by the contour boundary
    r_mask = ndimage.binary_fill_holes(r_mask)

    # Invert the mask since you want pixels outside of the region
    r_mask = np.multiply(~r_mask,255)
    
    return r_mask.astype('uint8') 


def draw_contours(img, contours):
    '''
        draw contours on an image
    '''
    # if not RGB, convert 
    if not len(np.shape(img)) == 3:
        cdraw_img = np.array(np.zeros((np.shape(img)[0],np.shape(img)[1],3)))
        cdraw_img[:,:,0],cdraw_img[:,:,1],cdraw_img[:,:,2] = img,img,img 

    for contour in contours:
        cdraw_img[contour[:, 0].astype(int), contour[:, 1].astype(int)] = [255,0,0]

    return cdraw_img


def particle_crop(img,contour):
    '''
        Use skimage contours to produce crop of individual.

        Make area outside of contour white
    '''
    xmin,xmax       = int(min(contour[:, 1])), int(max(contour[:, 1]))+1
    ymin,ymax       = int(min(contour[:, 0])), int(max(contour[:, 0]))+1
    # print ymin,ymax 
    # print xmin, xmax
    bwidth,bheight  = xmax-xmin, ymax-ymin
    # print np.shape(contour)
    cropmask        = np.array(np.zeros((bheight,bwidth)),dtype=bool)
    # print np.shape(cropmask)
    # print np.subtract(contour[:, 0],ymin).astype(int)
    # print np.subtract(contour[:, 1],xmin).astype(int)
    # Create a contour image by using the contour coordinates rounded to their nearest integer value
    cropmask[np.subtract(contour[:, 0],ymin).astype(int), np.subtract(contour[:, 1],xmin).astype(int)] = 1

    # Fill in the hole created by the contour boundary
    cropmask = np.multiply(ndimage.morphology.binary_fill_holes(cropmask),255).astype('uint8')
    zeroidx     = cropmask == 0
    onesidx     = cropmask == 255
    plktor.image.io.save_image(cropmask,'0mask.png')

    crop            = np.multiply(np.array(np.ones((bheight,bwidth))),255,dtype=float)
    crop            = img[ymin:ymax,xmin:xmax]
    crop[zeroidx]   = 255

    crop        = np.clip(img[ymin:ymax,xmin:xmax],0,255)
    
    # Remove pixels outside of contours 
    # crop            = np.subtract(crop,cropmask)

    return crop