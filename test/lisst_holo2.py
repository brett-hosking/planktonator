'''
    Crop individuals from LISST-Holo2 data
'''
try:
    import planktonator as plktor
except:
    from context import planktonator as plktor
import os

# Get the from deployment file
lat     = -52.690000
lon     = -40.125000
date    = 20171116
time    = 100900

project = 'ecotaxa_003_event'
 
mon_height, mon_width = 1230,1600 # determine automatically

# Path to images to extract particles from
path        = '../img/'
# path        = 'J:/DY086/LISST-HOLO/reconstructed/event_98'

# Path for particles to be saved to
output      = '../particles/'
# output      = 'J:/DY086/LISST-HOLO/reconstructed/event_98_particles'

# Run Planktonator Particle Extractor
plktor.run.extract_particles(path,output)

# Run Planktonator Particle Measurements 
plktor.run.measure_particles(output,mon_height,mon_width,project=project,lat=lat,lon=lon,date=date,time=time)

# Zip Data
plktor.tools.zipcompress(output,zipfile=os.path.join(path,project))

# Remove temporary files
if os.path.exists(output):plktor.tools.rmfolder(output)