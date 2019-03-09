import shutil

def zipcompress(path,zipf='ecotaxa.zip'):
    shutil.make_archive(zipf, 'zip', path)


def zipextract(path,zipf):
    '''
        shutil method may not work on windows
    '''
    try:
        shutil.unpack_archive(zipf,path)
    except:
        import zipfile
        zip_ref = zipfile.ZipFile(zipf, 'r')
        zip_ref.extractall(path)
        zip_ref.close()


def rmfolder(path):
    shutil.rmtree(path)


def rmspace(string):
    '''
        Remove arbitrary whitespace
    '''
    # remove space before and after string and all but one in the middle
    return re.sub(' +', ' ',string.strip())