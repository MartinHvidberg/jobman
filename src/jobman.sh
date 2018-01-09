#!/bin/bash

# make sure /worker and /Executables exists
mkdir workers
mkdir Executables

# refresh jobman.py from git  -- Optional
cp ~/git/jobman/src/jobman.py .

# refresh /Executables from Master  -- Optional
cp ~/git/PGV4/2018a/6_pgv_gv/beliggenhed/haeldning/demstat*.py ./Executables

#run
python ./jobman.py

