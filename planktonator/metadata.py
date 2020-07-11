import pandas as pd
import numpy as np
from planktonator.version import __version__

class ParticleMeasure:

    def __init__(self):
        self.df         = pd.DataFrame(columns=self.headers())

    def save(self,output):
        self.df.to_csv(output,index=False)

    def load(self,file):
        self.df = pd.read_csv(file)

    def subset(self,header='depth',val=0.0):
        '''
        remove any entries with values in header less 
        than val

        ignore index 0
        '''
        # self.df = self.df.loc[np.insert(pd.to_numeric(self.df[header].loc[1:]).values >= val,0,True)]
        self.df     = self.df.loc[self.df[header] >= val]

    def headers(self):
        return [
                'planktonator_particle_id',
                'montage_id',
                'deployment',
                'montage_num',
                'cast', 
                'year',	'month', 'day',	'hour',	'minute', 'second',
                'depth',
                'particle_centre_x',
                'particle_centre_y',	
                'particle_bbox_width',	
                'particle_bbox_height',
                'otsu_area', 'otsu_length', 'otsu_hull', 'otsu_threshold',
                'isodata_area', 'isodata_length','isodata_hull','isodata_threshold',
                'li_area', 'li_length','li_hull','li_threshold',
                'mean_area','mean_length','mean_hull','mean_threshold',
                'triangle_area','triangle_length','triangle_hull','triangle_threshold',
                'yen_area','yen_length','yen_hull','yen_threshold',
                'software_name',
                'software_version'
            ]

    def addrow( self,
                planktonator_particle_id=None,
                planktonator_montage_id=None,
                deployment=None,
                montage_number=None,
                cast=None,
                year=None,
                month=None,
                day=None,
                hour=None,
                minute=None,
                second=None,
                depth=None,
                particle_centre_x=None,
                particle_centre_y=None,	
                particle_bbox_width=None,	
                particle_bbox_height=None,
                otsu_area=None,otsu_length=None,otsu_hull=None,otsu_threshold=None,
                iso_area=None,iso_length=None,iso_hull=None,iso_threshold=None,
                li_area=None,li_length=None,li_hull=None,li_threshold=None,
                mean_area=None,mean_length=None,mean_hull=None,mean_threshold=None,
                triangle_area=None,triangle_length=None,triangle_hull=None,triangle_threshold=None,
                yen_area=None,yen_length=None,yen_hull=None,yen_threshold=None,
                software_name='planktonator',
                software_version=__version__
            ):
            self.df.loc[len(self.df)]   = [
                planktonator_particle_id,
                planktonator_montage_id,
                deployment,
                montage_number,
                cast,
                year,
                month,
                day,
                hour,
                minute,
                second,
                depth,
                particle_centre_x,
                particle_centre_y,	
                particle_bbox_width,	
                particle_bbox_height,
                otsu_area,otsu_length,otsu_hull,otsu_threshold,
                iso_area,iso_length,iso_hull,iso_threshold,
                li_area,li_length,li_hull,li_threshold,
                mean_area,mean_length,mean_hull,mean_threshold,
                triangle_area,triangle_length,triangle_hull,triangle_threshold,
                yen_area,yen_length,yen_hull,yen_threshold,
                software_name,
                software_version
            ]

class HoloBatch:

    def __init__(self):
        self.df         = pd.DataFrame(columns=self.headers())

    def save(self,output):
        self.df.to_csv(output,index=False)

    def load(self,file):
        self.df = pd.read_csv(file)

    def addrow( self,
                planktonator_particle_id=None,
                planktonator_montage_id=None,
                Area=None,
                EquivDiameter=None,
                MajorAxisLength=None,
                MinorAxisLength=None,
                Solidity=None,
                Eccentricity=None,
                FilledArea=None,
                ConvexArea=None,
                EquivAreaDiameter=None,
                Volume=None,
                Centroid=None,
                Depth=None,
                BoundingBox=None,
                Orientation=None,
                EulerNumber=None,
                Extent=None,
                Perimeter=None,
                software_name='planktonator',
                software_version=__version__
            ):
            self.df.loc[len(self.df)]   = [
                planktonator_particle_id,
                planktonator_montage_id,
                Area,
                EquivDiameter,
                MajorAxisLength,
                MinorAxisLength,
                Solidity,
                Eccentricity,
                FilledArea,
                ConvexArea,
                EquivAreaDiameter,
                Volume,
                Centroid,
                Depth,
                BoundingBox,
                Orientation,
                EulerNumber,
                Extent,
                Perimeter,
                software_name,
                software_version
            ]

    def headers(self):
        return [
                'planktonator_particle_id',
                'planktonator_montage_id',
                'Area',
                'EquivDiameter',
                'MajorAxisLength',
                'MinorAxisLength',
                'Solidity',
                'Eccentricity',
                'FilledArea',
                'ConvexArea',
                'EquivAreaDiameter',
                'Volume',
                'Centroid',
                'Depth',
                'BoundingBox',
                'Orientation',
                'EulerNumber',
                'Extent',
                'Perimeter',
                'software_name',
                'software_version'
            ]


class Annotation:

    def __init__(self):
        self.df         = pd.DataFrame(columns=self.headers())

    def save(self,output):
        self.df.to_csv(output,index=False)

    def load(self,file):
        self.df = pd.read_csv(file)

    def addrow( self,
                particle_id=None,
                montage_id=None,
                centre_x=None,
                centre_y=None,
                bbox_width=None,
                bbox_height=None,
                software_name='planktonator',
                software_version=__version__
            ):
            self.df.loc[len(self.df)]   = [
                particle_id,
                montage_id,
                centre_x,
                centre_y,
                bbox_width,
                bbox_height,
                software_name,
                software_version
            ]

    def headers(self):
        return [
                'particle_id',
                'montage_id',
                'centre_x',
                'centre_y',
                'bbox_width',
                'bbox_height',
                'software_name',
                'software_version'
            ]

class EcoTaxa:

    def __init__(self):

        self.columns,self.types    = self.headers()
        self.df         = pd.DataFrame(columns=self.columns)
        # add second row of headers 
        self.df.loc[0]  = self.types

    def save(self,output,index=False):
        self.df.to_csv(output,index=index,sep="\t")

    def loadtsv(self,file):
        self.df = pd.read_csv(file,delimiter="\t")

    def subset(self,header='object_major',val=None):
        '''
        remove any entries with values in header less 
        than val

        ignore index 0
        '''
        self.df = self.df.loc[np.insert(pd.to_numeric(self.df[header].loc[1:]).values >= val,0,True)]

    def depthsubset(self,threshold):
        '''
        remove any entries with depth values less than 
        the given threshold
        '''

    def addrow(self,img_file_name=None,
                    img_rank=None,
                    object_id=None,	
                    object_link=None,	
                    object_lat=None,	
                    object_lon=None,	
                    object_date=None,	
                    object_time=None,	
                    object_depth_min=None,	
                    object_depth_max=None,	
                    object_lat_end=None,	
                    object_lon_end=None,	
                    object_area=None,	
                    object_mean=None,	
                    object_stddev=None,	
                    object_mode=None,	
                    object_min=None,	
                    object_max=None,	
                    object_x=None,	
                    object_y=None,	
                    object_xm=None,	
                    object_ym=None,	
                    object_perim=None,	
                    object_bx=None,	
                    object_by=None,	
                    object_width=None,	
                    object_height=None,	
                    object_major=None,	
                    object_minor=None,	
                    object_angle=None,	
                    object_circ=None,	
                    object_feret=None,	
                    object_intden=None,	
                    object_median=None,	
                    object_skew=None,	
                    object_kurt=None,	
                    object_percentarea=None,	
                    object_xstart=None,	
                    object_ystart=None,	
                    object_area_exc=None,	
                    object_fractal=None,	
                    object_skelarea=None,	
                    object_tag=None,	
                    object_esd=None,	
                    object_elongation=None,	
                    object_range=None,	
                    object_meanpos=None,	
                    object_centroids=None,	
                    object_cv=None,	
                    object_sr=None,	
                    object_perimareaexc=None,	
                    object_feretareaexc=None,	
                    object_perimferet=None,	
                    object_perimmajor=None,	
                    object_circex=None,	
                    object_cdexc=None,	
                    process_id=None,	
                    process_date=None,	
                    process_time=None,	
                    process_img_software_version=__version__,
                    process_img_resolution=None,	
                    process_img_od_grey=None,	
                    process_img_od_std=None,	
                    process_img_background_img=None,	
                    process_particle_version=None,	
                    process_particle_threshold=None,	
                    process_particle_pixel_size_mm=None,	
                    process_particle_min_size_mm=None,	
                    process_particle_max_size_mm=None,	
                    process_particle_sep_mask=None,	
                    process_particle_bw_ratio=None,
                    process_software='planktonator',	
                    acq_id=None,
                    acq_min_mesh=None,	
                    acq_max_mesh=None,	
                    acq_sub_part=None,	
                    acq_sub_method=None,	
                    acq_hardware=None,	
                    acq_software=None,	
                    acq_author=None,	
                    acq_imgtype=None,	
                    acq_scan_date=None,	
                    acq_scan_time=None,	
                    acq_quality=None,	
                    acq_bitpixel=None,	
                    acq_greyfrom=None,	
                    acq_scan_resolution=None,	
                    acq_rotation=None,	
                    acq_miror=None,	
                    acq_xsize=None,	
                    acq_ysize=None,	
                    acq_xoffset=None,	
                    acq_yoffset=None,	
                    acq_lut_color_balance=None,	
                    acq_lut_filter=None,	
                    acq_lut_min=None,	
                    acq_lut_max=None,	
                    acq_lut_odrange=None,	
                    acq_lut_ratio=None,	
                    acq_lut_16b_median=None,	
                    acq_instrument=None,	
                    sample_id=None,	
                    sample_scan_operator=None,	
                    sample_ship=None,	
                    sample_program=None,	
                    sample_stationid=None,	
                    sample_bottomdepth=None,	
                    sample_ctdrosettefilename=None,	
                    sample_other_ref=None,	
                    sample_tow_nb=None,	
                    sample_tow_type=None,	
                    sample_net_type=None,	
                    sample_net_mesh=None,	
                    sample_net_surf=None,	
                    sample_zmax=None,	
                    sample_zmin=None,	
                    sample_tot_vol=None,	
                    sample_comment=None,	
                    sample_tot_vol_qc=None,	
                    sample_depth_qc=None,	
                    sample_sample_qc=None,	
                    sample_barcode=None,	
                    sample_duration=None,	
                    sample_ship_speed=None,	
                    sample_cable_length=None,	
                    sample_cable_angle=None,	
                    sample_cable_speed=None,	
                    sample_nb_jar=None,	
                    sample_dataportal_descriptor=None,	
                    sample_open=None):

        self.df.loc[len(self.df)]   =   [img_file_name,
                                        img_rank,
                                        object_id,	
                                        object_link,	
                                        object_lat,	
                                        object_lon,	
                                        object_date,	
                                        object_time,	
                                        object_depth_min,	
                                        object_depth_max,	
                                        object_lat_end,	
                                        object_lon_end,	
                                        object_area,	
                                        object_mean,	
                                        object_stddev,	
                                        object_mode,	
                                        object_min,	
                                        object_max,	
                                        object_x,	
                                        object_y,	
                                        object_xm,	
                                        object_ym,	
                                        object_perim,	
                                        object_bx,	
                                        object_by,	
                                        object_width,	
                                        object_height,	
                                        object_major,	
                                        object_minor,	
                                        object_angle,	
                                        object_circ,	
                                        object_feret,	
                                        object_intden,	
                                        object_median,	
                                        object_skew,	
                                        object_kurt,	
                                        object_percentarea,	
                                        object_xstart,	
                                        object_ystart,	
                                        object_area_exc,	
                                        object_fractal,	
                                        object_skelarea,	
                                        object_tag,	
                                        object_esd,	
                                        object_elongation,	
                                        object_range,	
                                        object_meanpos,	
                                        object_centroids,	
                                        object_cv,	
                                        object_sr,	
                                        object_perimareaexc,	
                                        object_feretareaexc,	
                                        object_perimferet,	
                                        object_perimmajor,	
                                        object_circex,	
                                        object_cdexc,	
                                        process_id,	
                                        process_date,	
                                        process_time,	
                                        process_img_software_version,
                                        process_img_resolution,	
                                        process_img_od_grey,	
                                        process_img_od_std,	
                                        process_img_background_img,	
                                        process_particle_version,	
                                        process_particle_threshold,	
                                        process_particle_pixel_size_mm,	
                                        process_particle_min_size_mm,	
                                        process_particle_max_size_mm,	
                                        process_particle_sep_mask,	
                                        process_particle_bw_ratio,
                                        process_software,	
                                        acq_id,	
                                        acq_min_mesh,	
                                        acq_max_mesh,	
                                        acq_sub_part,	
                                        acq_sub_method,	
                                        acq_hardware,	
                                        acq_software,	
                                        acq_author,	
                                        acq_imgtype,	
                                        acq_scan_date,	
                                        acq_scan_time,	
                                        acq_quality,	
                                        acq_bitpixel,	
                                        acq_greyfrom,	
                                        acq_scan_resolution,	
                                        acq_rotation,	
                                        acq_miror,	
                                        acq_xsize,	
                                        acq_ysize,	
                                        acq_xoffset,	
                                        acq_yoffset,	
                                        acq_lut_color_balance,	
                                        acq_lut_filter,	
                                        acq_lut_min,	
                                        acq_lut_max,	
                                        acq_lut_odrange,	
                                        acq_lut_ratio,	
                                        acq_lut_16b_median,	
                                        acq_instrument,	
                                        sample_id,	
                                        sample_scan_operator,	
                                        sample_ship,	
                                        sample_program,	
                                        sample_stationid,	
                                        sample_bottomdepth,	
                                        sample_ctdrosettefilename,	
                                        sample_other_ref,	
                                        sample_tow_nb,	
                                        sample_tow_type,	
                                        sample_net_type,
                                        sample_net_mesh,	
                                        sample_net_surf,	
                                        sample_zmax,	
                                        sample_zmin,	
                                        sample_tot_vol,	
                                        sample_comment,	
                                        sample_tot_vol_qc,	
                                        sample_depth_qc,	
                                        sample_sample_qc,	
                                        sample_barcode,	
                                        sample_duration,	
                                        sample_ship_speed,	
                                        sample_cable_length,	
                                        sample_cable_angle,	
                                        sample_cable_speed,	
                                        sample_nb_jar,	
                                        sample_dataportal_descriptor,	
                                        sample_open]

        
        
    

    
    def headers(self):
    
        '''
        img_file_name
        img_rank	
        object_id	
        object_link	
        object_lat	
        object_lon	
        object_date	
        object_time	
        object_depth_min	
        object_depth_max	
        object_lat_end	
        object_lon_end	
        object_area	
        object_mean	
        object_stddev	
        object_mode	
        object_min	
        object_max	
        object_x	
        object_y	
        object_xm	
        object_ym	
        object_perim.	
        object_bx	
        object_by	
        object_width	
        object_height	
        object_major	
        object_minor	
        object_angle	
        object_circ.	
        object_feret	
        object_intden	
        object_median	
        object_skew	
        object_kurt	
        object_%area	
        object_xstart	
        object_ystart	
        object_area_exc	
        object_fractal	
        object_skelarea	
        object_tag	
        object_esd	
        object_elongation	
        object_range	
        object_meanpos	
        object_centroids	
        object_cv	
        object_sr	
        object_perimareaexc	
        object_feretareaexc	
        object_perimferet	
        object_perimmajor	
        object_circex	
        object_cdexc	
        process_id	
        process_date	
        process_time	
        process_img_software_version
        process_img_resolution	
        process_img_od_grey	
        process_img_od_std	
        process_img_background_img	
        process_particle_version	
        process_particle_threshold	
        process_particle_pixel_size_mm	
        process_particle_min_size_mm	
        process_particle_max_size_mm	
        process_particle_sep_mask	
        process_particle_bw_ratio
        process_software	
        acq_id	
        acq_min_mesh	
        acq_max_mesh	
        acq_sub_part	
        acq_sub_method	
        acq_hardware	
        acq_software	
        acq_author	
        acq_imgtype	
        acq_scan_date	
        acq_scan_time	
        acq_quality	
        acq_bitpixel	
        acq_greyfrom	
        acq_scan_resolution	
        acq_rotation	
        acq_miror	
        acq_xsize	
        acq_ysize	
        acq_xoffset	
        acq_yoffset	
        acq_lut_color_balance	
        acq_lut_filter	
        acq_lut_min	
        acq_lut_max	
        acq_lut_odrange	
        acq_lut_ratio	
        acq_lut_16b_median	
        acq_instrument	
        sample_id	
        sample_scan_operator	
        sample_ship	
        sample_program	
        sample_stationid	
        sample_bottomdepth	
        sample_ctdrosettefilename	
        sample_other_ref	
        sample_tow_nb	
        sample_tow_type	
        sample_net_type	
        sample_net_mesh	
        sample_net_surf	
        sample_zmax	
        sample_zmin	
        sample_tot_vol	
        sample_comment	
        sample_tot_vol_qc	
        sample_depth_qc	
        sample_sample_qc	
        sample_barcode	
        sample_duration	
        sample_ship_speed	
        sample_cable_length	
        sample_cable_angle	
        sample_cable_speed	
        sample_nb_jar	
        sample_dataportal_descriptor	
        sample_open
        '''

        columns = np.array([    
                    ['img_file_name',   '[t]'],
                    ['img_rank',        '[f]'],
                    ['object_id',       '[f]'],
                    ['object_link',     '[t]'],	
                    ['object_lat',	    '[f]'],
                    ['object_lon',      '[f]'],	
                    ['object_date',     '[t]'],	
                    ['object_time',     '[t]'],	
                    ['object_depth_min','[f]'],
                    ['object_depth_max','[f]'],	
                    ['object_lat_end',  '[f]'],
                    ['object_lon_end',  '[f]'],
                    ['object_area',     '[f]'],
                    ['object_mean',     '[f]'],
                    ['object_stddev',   '[f]'],
                    ['object_mode',     '[f]'],
                    ['object_min',      '[f]'],
                    ['object_max',      '[f]'],
                    ['object_x',        '[f]'],
                    ['object_y',        '[f]'],
                    ['object_xm',       '[f]'],
                    ['object_ym',       '[f]'],
                    ['object_perim.',   '[f]'],	
                    ['object_bx',       '[f]'],
                    ['object_by',       '[f]'],
                    ['object_width',    '[f]'],	
                    ['object_height',   '[f]'],	
                    ['object_major',    '[f]'],
                    ['object_minor',    '[f]'],
                    ['object_angle',    '[f]'],
                    ['object_circ.',    '[f]'],
                    ['object_feret',    '[f]'],
                    ['object_intden',   '[f]'],
                    ['object_median',   '[f]'],
                    ['object_skew',     '[f]'],
                    ['object_kurt',     '[f]'],
                    ['object_%area',    '[f]'],
                    ['object_xstart',   '[f]'],
                    ['object_ystart',   '[f]'],
                    ['object_area_exc', '[f]'],	
                    ['object_fractal',      '[f]'],	
                    ['object_skelarea',     '[f]'],	
                    ['object_tag',          '[f]'],
                    ['object_esd',          '[f]'],  
                    ['object_elongation',   '[f]'],	
                    ['object_range',        '[f]'],
                    ['object_meanpos',      '[f]'],	
                    ['object_centroids',    '[f]'],	
                    ['object_cv',           '[f]'],
                    ['object_sr',           '[f]'],
                    ['object_perimareaexc', '[f]'],	
                    ['object_feretareaexc', '[f]'],	
                    ['object_perimferet',   '[f]'],
                    ['object_perimmajor',   '[f]'],
                    ['object_circex',       '[f]'],
                    ['object_cdexc',        '[f]'],
                    ['process_id',          '[t]'],
                    ['process_date',        '[t]'],
                    ['process_time',        '[t]'],
                    ['process_img_software_version',    '[t]'],
                    ['process_img_resolution',          '[f]'],
                    ['process_img_od_grey',             '[f]'],
                    ['process_img_od_std',              '[f]'],
                    ['process_img_background_img',      '[t]'],	
                    ['process_particle_version',        '[t]'],            
                    ['process_particle_threshold',      '[f]'],	
                    ['process_particle_pixel_size_mm',	'[f]'],    
                    ['process_particle_min_size_mm',    '[f]'],
                    ['process_particle_max_size_mm',    '[f]'],
                    ['process_particle_sep_mask',       '[t]'],
                    ['process_particle_bw_ratio',       '[f]'],
                    ['process_software',                '[t]'],
                    ['acq_id',                          '[t]'],
                    ['acq_min_mesh',                    '[f]'],	
                    ['acq_max_mesh',                    '[f]'],	
                    ['acq_sub_part',                    '[f]'],    	
                    ['acq_sub_method',                  '[t]'],	
                    ['acq_hardware',                    '[t]'],
                    ['acq_software',                    '[t]'],
                    ['acq_author',                      '[t]'],
                    ['acq_imgtype',                     '[t]'],
                    ['acq_scan_date',                   '[t]'],
                    ['acq_scan_time',                   '[t]'],
                    ['acq_quality',                     '[t]'],
                    ['acq_bitpixel',                    '[f]'],
                    ['acq_greyfrom',                    '[f]'],
                    ['acq_scan_resolution',             '[f]'],	
                    ['acq_rotation',                    '[f]'],
                    ['acq_miror',                       '[f]'],
                    ['acq_xsize',                       '[f]'],
                    ['acq_ysize',                       '[f]'],
                    ['acq_xoffset',                     '[f]'],	
                    ['acq_yoffset',	                    '[f]'],
                    ['acq_lut_color_balance',           '[f]'],	
                    ['acq_lut_filter',                  '[f]'],
                    ['acq_lut_min',                     '[f]'],
                    ['acq_lut_max',                     '[f]'],
                    ['acq_lut_odrange',                 '[f]'],	
                    ['acq_lut_ratio',                   '[f]'],
                    ['acq_lut_16b_median',              '[f]'],	
                    ['acq_instrument',                  '[t]'],	
                    ['sample_id',                       '[t]'],
                    ['sample_scan_operator',            '[t]'],	
                    ['sample_ship',                     '[t]'],
                    ['sample_program',                  '[t]'],
                    ['sample_stationid',                '[t]'],
                    ['sample_bottomdepth',              '[f]'],
                    ['sample_ctdrosettefilename',       '[t]'],	
                    ['sample_other_ref',                '[t]'],	
                    ['sample_tow_nb',                   '[f]'],
                    ['sample_tow_type',                 '[t]'],	
                    ['sample_net_type',                 '[t]'],	
                    ['sample_net_mesh',                 '[f]'],	
                    ['sample_net_surf',	                '[f]'],
                    ['sample_zmax',                     '[f]'],
                    ['sample_zmin',                     '[f]'],
                    ['sample_tot_vol',                  '[f]'],
                    ['sample_comment',                  '[t]'],
                    ['sample_tot_vol_qc',               '[f]'],
                    ['sample_depth_qc',                 '[f]'],
                    ['sample_sample_qc',                '[f]'],
                    ['sample_barcode',                  '[t]'],
                    ['sample_duration',                 '[f]'],
                    ['sample_ship_speed',               '[f]'],
                    ['sample_cable_length',             '[f]'],	
                    ['sample_cable_angle',              '[f]'],	
                    ['sample_cable_speed',              '[f]'],	
                    ['sample_nb_jar',                   '[f]'],	
                    ['sample_dataportal_descriptor',    '[t]'],	
                    ['sample_open',                     '[t]']
                    
                ])
        return columns[:,0], columns[:,1]
    