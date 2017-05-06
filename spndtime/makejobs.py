
"""" Part of JobMan
This program is intended for test of JobMan.
It creates a subdir /Available and put 100 batch files in there
Each batch file (.bat on win) will call spndtime.py once
with one of the integers 1..100
Nothing more - quite pointless - but suited to test JobMan..."""

import os

print "Make jobs 1..100"

# Adjust for Linux/windows differences...
if os.name.lower() in ('unix', 'posix'):
    str_osep = "/"
    str_pyth = "python"
    str_oext = ".sh"
elif os.name.lower() in ('win'):
    str_osep = "\\"
    str_pyth = "C:\Python27\python.exe"
    str_oext = ".bat"
else:
    print "Can't understand OS named: {}".format(os.name)
    exit(101)

directory = "Available"+str_osep

if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(100):
    fil_bat = open("{}spndtime_{}{}".format(directory,str(i),str_oext),"w")
    fil_bat.write("{} spndtime.py {}\n".format(str_pyth,str(i)))
    fil_bat.close()

print "Done..."