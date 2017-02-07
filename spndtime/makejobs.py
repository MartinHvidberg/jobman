
"""" Part of JobMan
This program is intended for test of JobMan.
It creates a subdir /Available and put 100 batch files in there
Each batch file (.bat on win) will call spndtime.py once
with one of the integers 1..100
Nothing more - quite pointless - but suited to test JobMan..."""

import os


directory = "Available"
print "Make jobs 1..100 in {}".format(directory)

if not os.path.exists(directory):
    os.makedirs(directory)

for i in range(100):
    fil_bat = open(directory+r"\spndtime_{}.bat".format(str(i)),"w")
    fil_bat.write(r"C:\Python27\python.exe spndtime.py {}".format(i)+"\n")
    fil_bat.close()

print "Done..."