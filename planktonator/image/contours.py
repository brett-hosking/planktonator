import numpy as np

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

