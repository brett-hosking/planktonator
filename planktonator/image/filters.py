import numpy as np


def linear(filterwidth=30):
    '''
        Generate a 1D array of linear filter coefficients

        Parameters
        ----------

    '''
    olap = int((filterwidth+1)/2)
    return np.lib.pad(np.linspace(1,3,olap), (0,olap-1),'reflect')
    

def kernel2D(coeffs):
    '''
        Create a 2D normalised kernel from a 1D array

        Parameters
        ----------
        coeffs : numpy array
            1D numpy array of filter coefficients 

    '''
    size = len(coeffs)
    Unit = np.array(np.ones((size,size)),dtype=float)
    filtx = [coeffs]
    Kx = np.multiply(filtx,Unit)
    filty = [coeffs]
    Ky = np.multiply(Unit,np.transpose(filty))
    Kernel = np.multiply(Kx,Ky)
    Normalise = np.sum(Kernel)
    return np.divide(Kernel,Normalise)