import planktonator as plktor
import os
import shutil
import numpy as np
import datetime
from skimage.filters import threshold_otsu, threshold_isodata, threshold_li, threshold_mean,threshold_minimum, threshold_triangle, threshold_yen
from skimage import measure

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
        # mask        = plktor.image.apply.threshold(img,t=240) # TODO add option to apply a hard threshold
        mask        = plktor.image.threshold.otsu(img)

        # apply low pass filter 
        kernel  = plktor.image.filters.kernel2D(plktor.image.filters.linear(filterwidth=25))
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


def measure_particles(particle_path,mon_height,mon_width,pixellim=100,project='measure4ecotaxa',lat=None,lon=None,date=None,time=None,hbcomposite=None,depththreshold=0):
    '''
    EcoTaxa measurements 

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

    # HoloBatch composite file
    if not hbcomposite == None: dfcomp      = plktor.holobatch.composite(hbcomposite)


    for f in filelist:
        if not f.lower().endswith(imgext): continue
        filename,_    = os.path.splitext(f)

        montage_id  = f[:f.find('particle')-1]
        deployment  = int(montage_id[:montage_id.find('-')])
        image_num   = int(montage_id[montage_id.rfind('-')+1:])
        montage     = montage_id + '-mon'

        try:
            index   = dfcomp[(dfcomp['image_number'] == image_num) & (dfcomp['deployment_id'] == deployment)].index.tolist()
            depth   = float(dfcomp['depth'][index])

            if depth < depththreshold:
                os.remove(os.path.join(particle_path,f))
                continue

            if depth == None:
                os.remove(os.path.join(particle_path,f))
                continue

        except:
            depth = None

        # load image 
        img         = plktor.image.io.imread(os.path.join(particle_path,f))

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
                        img_rank=0, 
                        object_id=filename,
                        object_lat=lat ,
                        object_lon=lon , 
                        object_date=date ,
                        object_time=time, 
                        # metadata 
                        object_depth_min=depth,
                        object_depth_max=depth,
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
            dfholo.Centroid = dfholo.Centroid.replace('\s+', ' ', regex=True) 
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


def thresholding(pdir,output,cast=None,hbcomposite=None,annotation=None,depththreshold=-99):
    '''
    Run thresholding on each particle and produce measurements

    Parameters
    ----------
    pdir : str
        the directory containing the particle images 
    output : str
        path for output csv file
    '''
    # Load the particle measurement class 
    pmeasure    = plktor.metadata.ParticleMeasure()

    # files in directory 
    files       = os.listdir(pdir)

    # HoloBatch composite file
    if not hbcomposite == None: dfcomp      = plktor.holobatch.composite(hbcomposite)
    if not annotation == None: 
        annot      = plktor.metadata.Annotation()
        annot.load(annotation)

    for i in range(len(files)):
        try:
            image = plktor.image.io.imread(os.path.join(pdir,files[i]))
        except:
            continue
        vignette    = files[i][:-4]
        montage_id  = files[i][:files[i].find('particle')-1]
        deployment  = int(montage_id[:montage_id.find('-')])
        image_num   = int(montage_id[montage_id.rfind('-')+1:])
        montage     = montage_id + '-mon'

        try:
            index   = dfcomp['image_number'] == image_num
            year    = int(dfcomp['year'][index])
            month   = int(dfcomp['month'][index])
            day     = int(dfcomp['day'][index])
            hour    = int(dfcomp['hour'][index])
            minute  = int(dfcomp['minute'][index])
            second  = int(dfcomp['second'][index])
            depth   = float(dfcomp['depth'][index])

            if depth < depththreshold:continue

        except:
            year,month,day,hour,minute,second,depth = None,None,None,None,None,None,None

        try:
            pindex      = annot.df['particle_id'] == vignette
            particle_centre_x   = int(annot.df['centre_x'][pindex])
            particle_centre_y   = int(annot.df['centre_y'][pindex])
            particle_bbox_width = int(annot.df['bbox_width'][pindex])	
            particle_bbox_height= int(annot.df['bbox_height'][pindex])
        except:
            particle_centre_x,particle_centre_y,particle_bbox_width,particle_bbox_height = None,None,None,None

        #### OTSU ####
        otsu_thresh = threshold_otsu(image)
        binary = np.multiply(np.invert(image > otsu_thresh),255.0).astype(int)

        props = measure.regionprops(binary)
        otsu_area = props[0]['Area'] # area
        otsu_carea = props[0]['ConvexArea'] # hull
        otsu_rlength = round(plktor.image.stats.feret_diameter(binary),1) # length
        # esd = round(props[0]['EquivDiameter'],1)
        # solidity = round(props[0]['Solidity'],1)

        #### ISOData ####
        iso_thresh = threshold_isodata(image)
        binary = np.multiply(np.invert(image > iso_thresh),255.0).astype(int)
        props = measure.regionprops(binary)
        iso_area = props[0]['Area'] # area
        iso_carea = props[0]['ConvexArea'] # hull
        iso_rlength = round(plktor.image.stats.feret_diameter(binary),1) # length

        #### Li ####
        li_thresh = threshold_li(image)
        try:
            binary = np.multiply(np.invert(image > li_thresh),255.0).astype(int)
            props = measure.regionprops(binary)
            li_area = props[0]['Area'] # area
            li_carea = props[0]['ConvexArea'] # hull
            li_rlength = round(plktor.image.stats.feret_diameter(binary),1) # length
        except:
            li_thresh = None
            li_area = None
            li_carea = None
            li_rlength = None


        #### Mean ####
        mean_thresh = threshold_mean(image)
        binary = np.multiply(np.invert(image > mean_thresh),255.0).astype(int)
        props = measure.regionprops(binary)
        mean_area = props[0]['Area'] # area
        mean_carea = props[0]['ConvexArea'] # hull
        mean_rlength = round(plktor.image.stats.feret_diameter(binary),1) # length


        #### Triangle ####
        triangle_thresh = threshold_triangle(image)
        binary = np.multiply(np.invert(image > triangle_thresh),255.0).astype(int)
        props = measure.regionprops(binary)
        triangle_area = props[0]['Area'] # area
        triangle_carea = props[0]['ConvexArea'] # hull
        triangle_rlength = round(plktor.image.stats.feret_diameter(binary),1) # length

        #### Yen ####
        yen_thresh = threshold_yen(image)
        binary = np.multiply(np.invert(image > yen_thresh),255.0).astype(int)
        props = measure.regionprops(binary)
        yen_area = props[0]['Area'] # area
        yen_carea = props[0]['ConvexArea'] # hull
        yen_rlength = round(plktor.image.stats.feret_diameter(binary),1) # length


        pmeasure.addrow(
                    planktonator_particle_id=vignette,
                    planktonator_montage_id=montage,
                    deployment=deployment,
                    montage_number=image_num,
                    cast=cast,
                    year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second,
                    depth=depth,
                    particle_centre_x=particle_centre_x,
                    particle_centre_y=particle_centre_y,	
                    particle_bbox_width=particle_bbox_width,	
                    particle_bbox_height=particle_bbox_height,
                    otsu_area=otsu_area,otsu_length=otsu_rlength,otsu_hull=otsu_carea,otsu_threshold=otsu_thresh,
                    iso_area=iso_area,iso_length=iso_rlength,iso_hull=iso_carea,iso_threshold=iso_thresh,
                    li_area=li_area,li_length=li_rlength,li_hull=li_carea,li_threshold=li_thresh,
                    mean_area=mean_area,mean_length=mean_rlength,mean_hull=mean_carea,mean_threshold=mean_thresh,
                    triangle_area=triangle_area,triangle_length=triangle_rlength,triangle_hull=triangle_carea,triangle_threshold=triangle_thresh,
                    yen_area=yen_area,yen_length=yen_rlength,yen_hull=yen_carea,yen_threshold=yen_thresh
            )
    
    # pmeasure.subset(val=depththresold)
    pmeasure.save(output)