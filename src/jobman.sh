#!/bin/bash

# make sure /worker and /Executables exists
mkdir workers
mkdir Executables

# refresh jobman.py from git  -- Optional
cp ~/git/jobman/src/jobman.py .

# refresh /Executables from Master
cp /var/opt/jobman/master_udsi/Executables/* ./Executables

#run
python ./jobman.py
