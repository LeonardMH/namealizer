import sys

if sys.version_info[0] == 2:
    from namealizer import *
else:
    from namealizer.namealizer import *
