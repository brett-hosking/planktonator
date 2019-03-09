import numpy as np
import planktonator as plktor

def removebyarea(contours,t=50):
    '''
        Remove contours that have an area below a
        given threshold

        Parameters 
        ----------
        contours : array_like 
            an array containing pixel corrdinates of object contours
            (pixels,0:y 1:x)
        t : int 
            pixel area threshold. Contours with a pixel area smaller than 
            t will be removed

        Returns
        -------
        a new array of with an equal or fewer number of contours
    '''
    newlist = []
    for contour in contours:
        xmin,xmax       = min(contour[:, 1]), max(contour[:, 1])
        ymin,ymax       = min(contour[:, 0]), max(contour[:, 0])
        bwidth,bheight  = xmax-xmin, ymax-ymin
        if (bwidth *bheight) <= t: continue
        newlist.append(contour)

    return np.asarray(newlist)


def removebypos():
    '''
        Remove contours that are within a given 
        area of the image(s)
    '''

    raise NotImplementedError


def flatten(img, contours):
    '''
        Flatten all contours into a single 1D array

        Parameters 
        ----------
        img : array-like
            image containing particles

        contours : array-like 
            contour positions

        Returns
        -------
    '''
    for n, contour in enumerate(contours):
        crop,cropmask            = plktor.image.apply.particle_crop(img,contour,n)
        if n == 0: 
            arr = plktor.image.apply.flatten(crop,cropmask)
        else: 
            arr     = np.append(arr, plktor.image.apply.flatten(crop,cropmask))
    return arr


def possize(contour):
    '''
        Given a contour, determine and return the 
        centre x and y coordinate, and width and height 
        of the best fitting bounding box


        Parameters
        ----------

        Returns
        -------
        x
        y
        width
        height
        
    '''
    xmin,xmax       = int(min(contour[:, 1])), int(max(contour[:, 1]))
    ymin,ymax       = int(min(contour[:, 0])), int(max(contour[:, 0]))
    bwidth,bheight  = xmax-xmin, ymax-ymin
    return int(np.rint(xmin+(bwidth/2.0))),int(np.rint(ymin+(bheight/2.0))),bwidth,bheight