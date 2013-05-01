import os, sys, shutil, time
from datetime import datetime
from stat import *
import Image
'''from PIL import Image'''
from PIL.ExifTags import TAGS

QUIT_ON_ERROR = False

# NO slash at the end
photo_dir = "I:\Dropbox\Photos"

def get_files(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s (not a file)' % pathname

# try and get any metadata from the image
def get_exif(file):
    ret = {}
    try:
        i = Image.open(file)
        info = i._getexif()

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    except Exception:
        # very possible there are no tags.  this isn't really a problem, we'll fall back on other data
        return None

def visitfile(file):
    # ignore ini files
    if file[-3:].lower() == 'ini':
        return 
        
    print file,
    created = os.path.getctime(file)
    modified = os.path.getmtime(file)
    taken = get_exif(file)
    
    # if we got tags back, check to see if the camera gave us a datetime of when the picture was taken
    if taken:
        if 'DateTimeOriginal' in taken:
            try:
                taken = int(time.mktime(time.strptime(taken['DateTimeOriginal'], '%Y:%m:%d %H:%M:%S')))
            except Exception:
                print "Invalid date on this file: %s" % taken['DateTimeOriginal']
                if QUIT_ON_ERROR:
                    sys.exit(1)
        else:
            taken = None
    
    # we'll default to the modified date
    actual = modified
    # but if the created date is earlier, that's probably more representative of the era of the picture
    if created < modified:
        actual = created
    # but still, if the camera gave us data and it claims to be older than the file system, it's probably a better source.
    if taken and taken < actual:
        actual = taken
        
    # parse the date we decided on
    actual = datetime.fromtimestamp(actual)
    newdir = "%s\\%s\\%s\\%s" % (photo_dir, actual.year, actual.month, actual.day)
    
    # if this year/month/day directory doesn't exist, go ahead and make it
    if not os.path.exists(newdir):
        os.makedirs(newdir)

    # set the full path, including filename
    actualnewdir = "\\".join((newdir, os.path.basename(file)))
    if not os.path.exists(actualnewdir):
        print "-> %s" % actualnewdir,
        # sometimes this doesn't delete the old file
        shutil.move(file, newdir)
    print ''

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dir = photo_dir
    else:
        dir = sys.argv[1]
    get_files(dir, visitfile)