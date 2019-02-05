import planktonator as plktor
import os
import shutil
import numpy as np
import datetime

def extract_particles(inpath,outpath,pixellim=200,montage_str='mon'):
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
    
    ### ------------------------- ###

    # clear/create tmp folder 
    if os.path.exists(os.path.join(outpath,'tmp')):shutil.rmtree(os.path.join(outpath,'tmp'))
    tempfolder = os.mkdir(os.path.join(outpath,'tmp'))


    # cycle through images and extract particles 
    for f in filelist:
        if not f.lower().endswith(imgext): continue
        if montage_str not in f: continue
        filename    = os.path.splitext(f)[0]
        # load image 
        img         = plktor.image.io.imread(os.path.join(inpath,f))

        # apply threshold 
        mask        = plktor.image.apply.threshold(img,t=240)
        
        # remove scale bar - function needs a better name - some more general
        mask         = plktor.image.apply.removescale(mask, a=[1210,1230,0,350], p=255)
        # apply low pass filter 
        kernel  = plktor.image.filters.kernel2D(plktor.image.filters.linear(filterwidth=35))
        mask    = plktor.image.apply.convolution(mask,kernel) 
        
        # apply threshold 
        mask        = plktor.image.apply.threshold(mask,t=240)
        # plktor.image.io.save_image(mask,os.path.join(outpath,"".join((filename,'_mask2.png'))))

        # calculate contours 
        contours    = plktor.image.apply.find_contours(mask)
        # print "number of particles: ", len(contours)

        # fill in mask where there is a gap in blob - must be a better way of doing this!
        mask        = plktor.image.apply.maskfill(mask,contours)
        # plktor.image.io.save_image(mask,os.path.join(outpath,"".join((filename,'_mask3.png'))))
        # recalculate contours 
        contours    = plktor.image.apply.find_contours(mask)
        # print "number of particles after fill: ", len(contours)

        # filter contours based on area - remove any tiny ones that cannot be classified
        contours = plktor.image.contours.removebyarea(contours, t=pixellim)
        # print "number of particles after removebyarea: ", len(contours)


        # Mark contours on images 
        # imgcont     = plktor.image.apply.draw_contours(img, contours)
        # plktor.image.io.save_image(imgcont,os.path.join(outpath,"".join((filename,'_contours.png'))))

        # Create folder for particle crops 
        # particle_outpath = os.path.join(outpath,filename)
        # if not os.path.exists(particle_outpath): os.mkdir(particle_outpath)
        for n, contour in enumerate(contours):
            crop,cropmask            = plktor.image.apply.particle_crop(img,contour,n)
            # save crop and change filename to particle
            crop_filename   = "".join((filename.replace(montage_str,'particle'),'_',str(n) )) 
            crop_file       = "".join((crop_filename,'.png'))
            plktor.image.io.save_image(crop,os.path.join(outpath,crop_file))
            plktor.image.io.save_image(cropmask,os.path.join(outpath,'tmp',"".join((crop_filename,'_mask.png'))))



def measure_particles(particle_path,mon_height,mon_width,pixellim=100,project='',lat=None,lon=None,date=None,time=None):
    '''

    Parameters
    ----------
    particle_path : str
        path to images of individual particles

    '''

    # get list of files from path - better outside of function?
    filelist    = os.listdir(particle_path)

    # excepted image extensions
    imgext      = ('jpg','jpeg','png','tiff')

    # metadata - Ecotaxa
    ecotax      = plktor.metadata.EcoTaxa()

    
    # coding_output   = '../coding_output_particles'
    # if not os.path.exists(coding_output): os.mkdir(coding_output)

    for f in filelist:
        if not f.lower().endswith(imgext): continue
        filename,_    = os.path.splitext(f)

        # load image 
        img         = plktor.image.io.imread(os.path.join(particle_path,f))
        # try:
        #     img_height,img_width   = np.shape(img)
        # except:
        #     img_height,img_width, _   = np.shape(img)

        # apply threshold 
        mask        = plktor.image.apply.threshold(img,t=230)
        # plktor.image.io.save_image(mask,os.path.join(coding_output,"".join((filename,'_m1.png'))))

        # apply low pass filter 
        kernel  = plktor.image.filters.kernel2D(plktor.image.filters.linear(filterwidth=10))
        mask    = plktor.image.apply.convolution(mask,kernel)
        # plktor.image.io.save_image(mask,os.path.join(coding_output,"".join((filename,'_m1_filtermask.png'))))

        # apply threshold 
        mask        = plktor.image.apply.threshold(mask,t=240)
        # plktor.image.io.save_image(mask,os.path.join(coding_output,"".join((filename,'_m2.png'))))

        # calculate contours 
        contours    = plktor.image.apply.find_contours(mask)

        # fill in mask where there is a gap in blob - must be a better way of doing this!
        mask        = plktor.image.apply.maskfill(mask,contours)
        # plktor.image.io.save_image(mask,os.path.join(coding_output,"".join((filename,'_m3.png'))))

        # recalculate contours 
        contours    = plktor.image.apply.find_contours(mask)
        # print "number of particles after fill: ", len(contours)

        # filter contours based on area - remove any tiny ones that cannot be classified
        contours = plktor.image.contours.removebyarea(contours, t=pixellim)

        # if no contours exist - skip and also remove particle
        if len(contours) < 1:
            os.remove(os.path.join(particle_path,f))
            # print ('no contours')
            continue

        # Mark contours on images 
        imgcont     = plktor.image.apply.draw_contours(img, contours)
        # plktor.image.io.save_image(imgcont,os.path.join(coding_output,"".join((filename,'_contours.png'))))

        # Create 1D array of all contour data
        # cont_flat   = plktor.image.contours.flatten(img, contours)
        cont_flat   = plktor.image.apply.flatten(img, mask)

        #Particle parameters 
        obj_height,obj_width = plktor.image.stats.shape(img)

        # 1D array Calculations 
        area                    = plktor.image.stats.area(mask)
        mean                    = plktor.image.stats.mean(cont_flat)

        # Load single mask from extract_particles()
        mask_full               = plktor.image.io.imread(os.path.join(particle_path,'tmp',"".join((filename,"_mask.png"))))
        objmajor,objminor       = plktor.image.stats.majorminor(mask_full) 

        # Mask Calculations
        perim                   = plktor.image.stats.perimeter(mask,invert=True)     

        cdatetime = datetime.datetime.now()

        # add meta data - mask has white background and black objects, full mask has black background and white object
        ecotax.addrow(  img_file_name=f,
                        process_id='planktonator_' + project,
                        process_date=cdatetime.strftime("%Y%m%d"),
                        process_time=cdatetime.strftime("%H:%M:%S"),
                        img_rank=0, # ?
                        object_id=filename,
                        object_lat=lat ,
                        object_lon=lon , 
                        object_date=date ,
                        object_time=time, 
                        # Shape Calculations
                        object_width=obj_width, 
                        object_height=obj_height, 
                        # 1D Array Calculations
                        object_mean=mean,
                        object_area=area,
                        object_mode=plktor.image.stats.mode(cont_flat), 
                        object_max=plktor.image.stats.maxgrey(cont_flat),
                        object_min=plktor.image.stats.mingrey(cont_flat),
                        object_range=plktor.image.stats.rangegrey(cont_flat),
                        object_stddev=plktor.image.stats.std(cont_flat), 
                        object_median=plktor.image.stats.median(cont_flat),
                        object_percentarea=plktor.image.stats.area_proportion(area,mon_height,mon_width),
                        object_intden=plktor.image.stats.intden(mean,area),
                        object_meanpos=plktor.image.stats.meanpos(cont_flat),
                        object_cv=plktor.image.stats.coeffvar(cont_flat),
                        object_sr=plktor.image.stats.stdrange(cont_flat),
                        object_area_exc=plktor.image.stats.area(cont_flat),
                        # Mask Calculations
                        object_perim=perim,
                        object_circ=plktor.image.stats.circularity(mask,area,perim=perim),
                        object_skelarea=plktor.image.stats.skelarea(mask,invert=True),
                        # Full Mask Calculations
                        object_perimmajor=plktor.image.stats.perimmajor(perim,objmajor),
                        object_elongation=plktor.image.stats.perimmajor(objmajor,objminor),
                        object_major=objmajor,
                        object_minor=objminor 
                        # object_minor= , 
                        # object

                   )

    # save metadata
    ecotax.save(os.path.join(particle_path,project+'.tsv'))

    # remove temporary files
    if os.path.exists(os.path.join(particle_path,'tmp')):shutil.rmtree(os.path.join(particle_path,'tmp'))

# if __name__=='__main__':