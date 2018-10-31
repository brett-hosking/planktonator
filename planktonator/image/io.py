import numpy as np
import imageio

def imread(path):
    '''
        Use imageio library to load an image as a numpy array

        Parameters
        ----------
        path : string 
            path to the image file

        Returns
        ------- 
        image : array_like 
    '''
    return imageio.imread(path)


def save_image(arr,output):
    '''
        Use imageio library to save an image after clipping 
        the input between the range [0,255] and converting
        to unsigned 8-bit int

        Parameters
        ----------
        arr : numpy array 
            image array with either 1 (greyscale) or 3 (RGB)
            channels
        output : string 
            path to output

        Returns
        -------
        None
    '''
    imageio.imwrite(output,np.clip(arr,0,255).astype('uint8'))


def save_npy(arr,output):
    raise NotImplementedError