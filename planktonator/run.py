import planktonator as plktor
import os

def extract_particles(inpath,outpath):
    '''
    script for extracting particles from holographic images

    Parameters
    ----------
    inpath : str
        path to images containing particles to extract
    outpath : str
        path to save individual particle images
    Returns 
    -------
    '''
    # get list of files from path - better outside of function?
    filelist    = os.listdir(inpath)

    # create output directory 
    if not os.path.exists(outpath):os.mkdir(outpath)

    # excepted image extensions
    imgext      = ('jpg','jpeg','png','tiff')

    ### Parameters to add to func ###
    # pixel area limit
    pixellim    = 200
    ### ------------------------- ###

    # cycle through images and extract particles 
    for s in filelist:
        if not s.lower().endswith(imgext): continue
        filename    = os.path.splitext(s)[0]

        # load image 
        img         = plktor.image.io.imread(os.path.join(inpath,s))

        # apply threshold 
        mask        = plktor.image.apply.threshold(img,t=240)
        # plktor.image.io.save_image(mask,os.path.join(outpath,"".join((filename,'_mask1.png'))))
        # remove scale bar - function needs a better name - some more general
        mask         = plktor.image.apply.removescale(mask, a=[1210,1230,0,350], p=255)
        # apply low pass filter 
        kernel  = plktor.image.filters.kernel2D(plktor.image.filters.linear(filterwidth=35))
        mask    = plktor.image.apply.convolution(mask,kernel) 
        # plktor.image.io.save_image(mask,os.path.join(outpath,"".join((filename,'_filtermask.png'))))
        # apply threshold 
        mask        = plktor.image.apply.threshold(mask,t=240)
        # plktor.image.io.save_image(mask,os.path.join(outpath,"".join((filename,'_mask2.png'))))

        # calculate contours 
        contours    = plktor.image.apply.find_contours(mask)
        print "number of particles: ", len(contours)

        # fill in mask where there is a gap in blob - must be a better way of doing this!
        mask        = plktor.image.apply.maskfill(mask,contours)
        # plktor.image.io.save_image(mask,os.path.join(outpath,"".join((filename,'_mask3.png'))))
        # recalculate contours 
        contours    = plktor.image.apply.find_contours(mask)
        print "number of particles after fill: ", len(contours)

        # filter contours based on area - remove any tiny ones that cannot be classified
        contours = plktor.image.contours.removebyarea(contours, t=pixellim)
        print "number of particles after removebyarea: ", len(contours)


        # Mark contours on images 
        imgcont     = plktor.image.apply.draw_contours(img, contours)
        plktor.image.io.save_image(imgcont,os.path.join(outpath,"".join((filename,'_contours.png'))))
        for n, contour in enumerate(contours):
            crop           = plktor.image.apply.particle_crop(img,contour)
            # save crop
            plktor.image.io.save_image(crop,os.path.join(outpath,"".join((filename,'_',str(n),'.png'))))


# if __name__=='__main__':