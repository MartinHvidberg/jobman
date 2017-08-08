
"""" Part of JobMan
This program is intended for test of JobMan.
It creates a subdir /Available and put 'int_max' batch files in there.
Each batch file (.bat on win) will call spndtime.py once
with one of the integers 1..int_max
Nothing more - quite pointless - but suited to test JobMan..."""

import os

__version__ = '0.2'
__build__ = '2017-08-08 08:08'

int_max = 20

print "Make jobs 1..{}".format(int_max)

# Adjust for Linux/windows differences...
if os.name.lower() in ('unix', 'posix'):
    str_osep = "/"
    str_pyth = "python"
    str_oext = ".sh"
elif os.name.lower() in ('win', 'nt'):
    str_osep = "\\"
    str_pyth = "C:\Python27\python.exe"
    str_oext = ".bat"
else:
    str_osep = ""
    str_pyth = ""
    str_oext = ""
    print "Can't understand OS named: {}".format(os.name)
    exit(101)

directory = "Available" + str_osep

if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(int_max):
    fil_bat = open("{}spndtime_{}{}".format(directory, str(i), str_oext), "w")
    fil_bat.write("{0} ..{2}..{2}Executables{2}spndtime.py {1}\n".format(str_pyth, str(i), str_osep))
    fil_bat.close()

print "Done..."
