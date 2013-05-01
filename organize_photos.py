import os, sys, shutil, time
from datetime import datetime
from stat import *
import Image
'''from PIL import Image'''
from PIL.ExifTags import TAGS

QUIT_ON_ERROR = False

# NO slash at the end
photo_dir = "I:\Dropbox\Photos"

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[ST_MODE]
        #if S_ISDIR(mode):
            # It's a directory, recurse into it
            #walktree(pathname, callback)
        if S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def get_exif(fn):
    ret = {}
    try:
        i = Image.open(fn)
        info = i._getexif()

        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value
        return ret
    except Exception:
        return None

def visitfile(file):
    if file[-3:].lower() == 'ini':
        return 
        
    print file,
    created = os.path.getctime(file)
    modified = os.path.getmtime(file)
    taken = get_exif(file)
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
    
    actual = modified
    if created < modified:
        actual = created
    if taken and taken < actual:
        actual = taken
        
    actual = datetime.fromtimestamp(actual)
    newdir = "%s\\%s\\%s\\%s" % (photo_dir, actual.year, actual.month, actual.day)
    
    if not os.path.exists(newdir):
        os.makedirs(newdir)

    actualnewdir = "\\".join((newdir, os.path.basename(file)))
    if not os.path.exists(actualnewdir):
        print "-> %s" % actualnewdir,
        shutil.move(file, newdir)
    print ''

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dir = photo_dir
    else:
        dir = sys.argv[1]
    walktree(dir, visitfile)