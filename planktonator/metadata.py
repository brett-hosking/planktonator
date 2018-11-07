import pandas as pd

class EcoTaxa:

    def __init__(self):

        self.columns    = self.headers()
        self.df         = pd.DataFrame(columns=self.columns)


    def save(self,output,index=False):
        self.df.to_csv(output,index=index)

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
                    process_img_software_version=None,
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
                    process_software=None,	
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

        return ['img_file_name',
        'img_rank'	,
        'object_id'	,
        'object_link',	
        'object_lat',	
        'object_lon',	
        'object_date',	
        'object_time',	
        'object_depth_min',
        'object_depth_max',	
        'object_lat_end'	,
        'object_lon_end'	,
        'object_area'	,
        'object_mean'	,
        'object_stddev'	,
        'object_mode'	,
        'object_min'	,
        'object_max'	,
        'object_x'	,
        'object_y'	,
        'object_xm'	,
        'object_ym'	,
        'object_perim.',	
        'object_bx'	,
        'object_by'	,
        'object_width',	
        'object_height',	
        'object_major'	,
        'object_minor'	,
        'object_angle'	,
        'object_circ'	,
        'object_feret'	,
        'object_intden'	,
        'object_median'	,
        'object_skew'	,
        'object_kurt'	,
        'object_%area'	,
        'object_xstart'	,
        'object_ystart'	,
        'object_area_exc',	
        'object_fractal',	
        'object_skelarea',	
        'object_tag'	,
        'object_esd'	,
        'object_elongation',	
        'object_range'	,
        'object_meanpos',	
        'object_centroids',	
        'object_cv'	,
        'object_sr'	,
        'object_perimareaexc',	
        'object_feretareaexc',	
        'object_perimferet'	,
        'object_perimmajor'	,
        'object_circex'	,
        'object_cdexc'	,
        'process_id'	,
        'process_date'	,
        'process_time'	,
        'process_img_software_version',
        'process_img_resolution'	,
        'process_img_od_grey'	,
        'process_img_od_std'	,
        'process_img_background_img',	
        'process_particle_version'	,
        'process_particle_threshold',	
        'process_particle_pixel_size_mm',	
        'process_particle_min_size_mm'	,
        'process_particle_max_size_mm'	,
        'process_particle_sep_mask'	,
        'process_particle_bw_ratio',
        'process_software'	,
        'acq_id'	,
        'acq_min_mesh',	
        'acq_max_mesh',	
        'acq_sub_part',	
        'acq_sub_method',	
        'acq_hardware'	,
        'acq_software'	,
        'acq_author'	,
        'acq_imgtype'	,
        'acq_scan_date'	,
        'acq_scan_time'	,
        'acq_quality'	,
        'acq_bitpixel'	,
        'acq_greyfrom'	,
        'acq_scan_resolution',	
        'acq_rotation'	,
        'acq_miror'	,
        'acq_xsize'	,
        'acq_ysize'	,
        'acq_xoffset',	
        'acq_yoffset',	
        'acq_lut_color_balance',	
        'acq_lut_filter'	,
        'acq_lut_min'	,
        'acq_lut_max'	,
        'acq_lut_odrange',	
        'acq_lut_ratio'	,
        'acq_lut_16b_median',	
        'acq_instrument',	
        'sample_id'	,
        'sample_scan_operator',	
        'sample_ship'	,
        'sample_program'	,
        'sample_stationid'	,
        'sample_bottomdepth'	,
        'sample_ctdrosettefilename',	
        'sample_other_ref',	
        'sample_tow_nb'	,
        'sample_tow_type',	
        'sample_net_type',	
        'sample_net_mesh',	
        'sample_net_surf',	
        'sample_zmax'	,
        'sample_zmin'	,
        'sample_tot_vol'	,
        'sample_comment'	,
        'sample_tot_vol_qc'	,
        'sample_depth_qc'	,
        'sample_sample_qc'	,
        'sample_barcode'	,
        'sample_duration'	,
        'sample_ship_speed'	,
        'sample_cable_length',	
        'sample_cable_angle',	
        'sample_cable_speed',	
        'sample_nb_jar',	
        'sample_dataportal_descriptor',	
        'sample_open']

    