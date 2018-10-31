'''
    Crop individuals from LISST-Holo2 data
'''
try:
    import planktonator as plktor
except:
    from context import planktonator as plktor


# Path to images to extract particles from 
path        = '../img/'

# Output path for saving individual particles
output      = '../particles/'

# Run Planktonator!
plktor.run.extract_particles(path,output)