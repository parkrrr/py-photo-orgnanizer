PyPhotoOrgnanizer
=================

A small Python to organize photos based on date.  It will generally use created/modified dates from the file system, but will use DateTimeOriginal metadata if it exists.  It will then drop it into directories in this structure:

PhotoDirectory\Year\Month\Day

Requirements:
* Python 2.7
* [Python Image Library](http://www.pythonware.com/products/pil/)

Usage:
`organize_photos.py [photo diectory]`