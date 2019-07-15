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
    if not os.path.exists(os.path.join(outpath,'tmp')):os.makedirs(os.path.join(outpath,'tmp'))

    # Create annotation class 
    annot   = plktor.metadata.Annotation()

    # cycle through images and extract particles 
    for f in filelist:
        if not f.lower().endswith(imgext): continue
        if montage_str not in f: continue
        filename    = os.path.splitext(f)[0]
        # load image 
        img         = plktor.image.io.imread(os.path.join(inpath,f))

        # remove scale bar 
        img         = plktor.image.apply.removescale(img, a=[1205,1230,0,350], p=255)

        # apply threshold 
        # mask        = plktor.image.apply.threshold(img,t=240)
        mask        = plktor.image.threshold.otsu(img)

        # apply low pass filter 
        kernel  = plktor.image.filters.kernel2D(plktor.image.filters.linear(filterwidth=25))# 35
        mask    = plktor.image.apply.convolution(mask,kernel) 
        # apply threshold 
        mask        = plktor.image.apply.threshold(mask,t=240) # 240

        # calculate contours 
        contours    = plktor.image.apply.find_contours(mask)

        # fill in mask where there is a gap in blob - must be a better way of doing this!
        mask        = plktor.image.apply.maskfill(mask,contours)

        # recalculate contours 
        contours    = plktor.image.apply.find_contours(mask)

        # filter contours based on area - remove any tiny ones that cannot be classified
        contours = plktor.image.contours.removebyarea(contours, t=pixellim)

        # Mark contours on images 
        # imgcont     = plktor.image.apply.draw_contours(img, contours)

        # Create folder for particle crops 
        # particle_outpath = os.path.join(outpath,filename)
        # if not os.path.exists(particle_outpath): os.mkdir(particle_outpath)
        for n, contour in enumerate(contours):
            crop,cropmask            = plktor.image.apply.particle_crop(img,contour)
            # Get x and y, and bounding box width and height
            x,y,bwidth,bheight       = plktor.image.contours.possize(contour)
            # save crop and change filename to particle
            crop_filename   = "".join((filename.replace(montage_str,'particle'),'_',str(n) )) 
            crop_file       = "".join((crop_filename,'.png'))
            plktor.image.io.save_image(crop,os.path.join(outpath,crop_file))
            plktor.image.io.save_image(cropmask,os.path.join(outpath,'tmp',"".join((crop_filename,'_mask.png'))))

            # Add to annotation file 
            annot.addrow(
                        particle_id     = crop_filename,
                        montage_id      = filename,
                        centre_x        = x, 
                        centre_y        = y,
                        bbox_width      = bwidth,
                        bbox_height     = bheight
            )

    # save annotation file 
    annot.save(os.path.join(inpath,'particle_annotation.csv'))


def measure_particles(particle_path,mon_height,mon_width,pixellim=100,project='measurements',lat=None,lon=None,date=None,time=None):
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

        # apply low pass filter 
        kernel  = plktor.image.filters.kernel2D(plktor.image.filters.linear(filterwidth=10))
        mask    = plktor.image.apply.convolution(mask,kernel)

        # apply threshold 
        mask        = plktor.image.apply.threshold(mask,t=240)

        # calculate contours 
        contours    = plktor.image.apply.find_contours(mask)

        # fill in mask where there is a gap in blob 
        mask        = plktor.image.apply.maskfill(mask,contours)

        # recalculate contours 
        contours    = plktor.image.apply.find_contours(mask)

        # filter contours based on area - remove any tiny ones that cannot be classified
        contours = plktor.image.contours.removebyarea(contours, t=pixellim)

        # if no contours exist - skip and also remove particle
        if len(contours) < 1:
            os.remove(os.path.join(particle_path,f))
            continue

        # Mark contours on images 
        # imgcont     = plktor.image.apply.draw_contours(img, contours)

        # Create 1D array of all contour data
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


def holobatchsync(annotationdir, holobatchdir):
    '''
    match the particles detected by Planktonator 
    with those detected by Holo Batch using 
    closest centroids

    Parameters 
    ----------
    annotationdir : str 
        path to the annotation dir with file produced by extract_particles()
    holobatchdir : str 
        path to the holo batch size directory
    '''
    import pandas as pd
    ''' Read annotation file '''
    annot   = plktor.metadata.Annotation()
    annot.load(os.path.join(annotationdir, 'particle_annotation.csv'))

    ''' Create new HoloBatch annotation file '''
    holob   = plktor.metadata.HoloBatch()

    ''' for every particle find the best match from the holobatch output '''
    N       = len(annot.df)
    for i in range(N):
        xpos , ypos         = annot.df.iloc[i]['centre_x'],annot.df.iloc[i]['centre_y']
        montage_id  = annot.df.iloc[i]['montage_id']
        # Load holobatch file 
        try:
            dfholo      = pd.read_csv(os.path.join(holobatchdir, montage_id[:-4] + '-pstat.csv'))

             # for each particle in dfholo, calculate the euclidean distance 
            dfholo.Centroid = dfholo.Centroid.replace('\s+', ' ', regex=True) # USE this! should work for all
            # split the strings into two, x and y
            dfholo['centroid_x']    = pd.to_numeric(dfholo.Centroid.str.split(' ').str.get(0), errors='coerce')
            dfholo['centroid_y']    = pd.to_numeric(dfholo.Centroid.str.split(' ').str.get(1), errors='coerce')  
            # calculate euclidean distance between plantonator coordinates and all holobatch coordinates.
            dfholo['euclidean']     = np.sqrt(((dfholo['centroid_x'] - xpos)**2) + ((dfholo['centroid_y'] - ypos)**2))
            # determine the closest one 
            mineuclid               = dfholo['euclidean'].min() 
            match_id                = np.where(dfholo['euclidean'] == mineuclid)[0][0]
            # add row to holobatch metadata class
            holob.addrow(
                    planktonator_particle_id        = annot.df.iloc[i]['particle_id'],
                    planktonator_montage_id         = annot.df.iloc[i]['montage_id'],
                    Area                            = dfholo.iloc[match_id]['Area'],
                    EquivDiameter                   = dfholo.iloc[match_id]['EquivDiameter'],
                    MajorAxisLength                 = dfholo.iloc[match_id]['MajorAxisLength'],
                    MinorAxisLength                 = dfholo.iloc[match_id]['MinorAxisLength'],
                    Solidity                        = dfholo.iloc[match_id]['Solidity'],
                    Eccentricity                    = dfholo.iloc[match_id]['Eccentricity'],
                    FilledArea                      = dfholo.iloc[match_id]['FilledArea'],
                    ConvexArea                      = dfholo.iloc[match_id]['ConvexArea'],
                    EquivAreaDiameter               = dfholo.iloc[match_id]['EquivAreaDiameter'],
                    Volume                          = dfholo.iloc[match_id]['Volume'],
                    Centroid                        = dfholo.iloc[match_id]['Centroid'],
                    Depth                           = dfholo.iloc[match_id]['Depth'],
                    BoundingBox                     = dfholo.iloc[match_id]['BoundingBox'],
                    Orientation                     = dfholo.iloc[match_id]['Orientation'],
                    EulerNumber                     = dfholo.iloc[match_id]['EulerNumber'],
                    Extent                          = dfholo.iloc[match_id]['Extent'],
                    Perimeter                       = dfholo.iloc[match_id]['Perimeter']
            )
        except:
            # add row to holobatch metadata class
            holob.addrow(
                    planktonator_particle_id        = annot.df.iloc[i]['particle_id'],
                    planktonator_montage_id         = annot.df.iloc[i]['montage_id']
            )
        
        
    # save holobatch metadata 
    holob.save(os.path.join(annotationdir,'holobatch_annotation.csv'))
