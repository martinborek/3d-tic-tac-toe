'''
@author: xdobes13
'''

import sys
import Globals as globs

def dbg(something):
    if globs.DEBUG:
        sys.stderr.write("DEBUG: " + str(something)+"\n")
