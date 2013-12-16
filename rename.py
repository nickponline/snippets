import sys
import os
for filename in os.listdir(sys.argv[1]):
	if filename.endswith("mp3"):
		oldname = filename
		newname = filename[3:]
		print oldname, newname
		os.rename(oldname, newname)

import sys
import os
for filename in os.listdir(sys.argv[1]):
	if filename.endswith("mp3"):
		oldname = filename
		newname = filename[3:]
		print oldname, newname
		os.rename(oldname, newname)