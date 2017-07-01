Thanks for the help. I ended up writing a C DLL called PyKeyboardAccess.dll
and accessing the crt conio functions, exporting this routine:

#include <conio.h>

int kb_inkey () {
   int rc;
   int key;

   key = _kbhit();

   if (key == 0) {
      rc = 0;
   } else {
      rc = _getch();
   }

   return rc;
}

And I access it in python using the ctypes module (built into python 2.5):

import ctypes
import time

#
# first, load the DLL
#


try:
    kblib = ctypes.CDLL("PyKeyboardAccess.dll")
except:
    raise ("Error Loading PyKeyboardAccess.dll")


#
# now, find our function
#

try:
    kbfunc = kblib.kb_inkey
except:
    raise ("Could not find the kb_inkey function in the dll!")


#
# Ok, now let's demo the capability
#

while 1:
    x = kbfunc()

    if x != 0:
        print "Got key: %d" % x
    else:
        time.sleep(.01)