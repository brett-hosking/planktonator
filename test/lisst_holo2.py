'''
    Crop individuals from LISST-Holo2 data
'''
# try:
import planktonator as plktor
# except:
#     from context import planktonator as plktor
import os

# Get the from deployment file
def deployment(cruise, event):

    if cruise == 'DY086':
        if event==34:
            # ''' Event 34 ''' 
            lat     = -52.690000
            lon     = -40.125000
            date    = 20171116
            time    = 100900
        # elif event==98:
        #     # ''' Event 98 ''' 
        #     lat     = -52.775333
        #     lon     = -40.349333
        #     date    = 20171120
        #     time    = 235000
        elif event==120:
            # ''' Event 120 ''' 
            lat     = -56.400000
            lon     = -41.216667
            date    = 20171124
            time    = 013500
        # elif event == 145:
        #      # ''' Event 145 ''' 
        #     lat     = -56.633333
        #     lon     = -40.916667
        #     date    = 20171125
        #     time    = 161500
    elif cruise == 'DY090':
        if event == 154:
            lat     = -18.0198
            lon     = 11.0084
            date    = 20180604
            time    = 050300
        elif event == 167: 
            lat     = -18.0197
            lon     = 11.00845
            date    = 20180605
            time    = 014300
        elif event == 198: 
            lat     = -18.0196
            lon     = 11.00822
            date    = 20180606
            time    = 231600


    return lat,lon,date,time

cruise  = 'DY090'
event   = 154
lat,lon,date,time = deployment(cruise,event)
project = 'ecotaxa_' + cruise + '_event' + str(event)
mon_height, mon_width = 1230,1600 # determine automatically

# Path to images to extract particles from
# path        = '../img/'
path        = 'J:/' + str(cruise) + '/LISST-HOLO/reconstructed/event_' + str(event)
sizepath    = 'J:/' + str(cruise) + '/LISST-HOLO/size/event_' + str(event)

# Path for particles to be saved to
# output      = '../particles/'
output      = 'J:/' + str(cruise) + '/LISST-HOLO/reconstructed/event_' + str(event) + '_particles'

# Run Planktonator Particle Extractor
# plktor.run.extract_particles(path,output)

# Match Planktonator annotations to Holo Batch size distributions to get depth
plktor.run.holobatchsync(path,sizepath)

# Run Planktonator Particle Measurements 
# plktor.run.measure_particles(output,mon_height,mon_width,project=project,lat=lat,lon=lon,date=date,time=time)

# Zip Data
# plktor.tools.zipcompress(output,zipf=os.path.join(path,project))

# Remove temporary files
if os.path.exists(output):plktor.tools.rmfolder(output)