import os, os.path

dirtocheck = "/home/nickp/work/"

for root, dirs, files in os.walk(dirtocheck):
    for f in files:
        fullpath = os.path.join(root, f)
        print fullpath
        if os.path.getsize(fullpath) < 200 * 1024:
            os.remove(fullpath)