
""" Job Man
Read .config file

Delete all local files, i.e empty local work-directory
Look through /Available and pick a job
Move that job file to /Busy
Make a copy of it to local work-directory
Execute the file locally
If exist success.jobman in local dir, then
    move job file from /Busy to /Completed, else
    move job tile from /Busy to /Discarded
Delete all local files, i.e empty local work-directory"""

import os, sys
import shutil
import random

def clear_dir(dirpath):
    if os.path.exists(dirpath):
        for filename in os.listdir(dirpath):
            filepath = os.path.join(dirpath, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)
    else:
        os.makedirs(dirpath)

delim_dir = "\\"
# XXX Should be a argv...
str_master_dir = r"C:\Martin\Work_github\jobman\jobman_master"

dic_config = dict()
fil_conf = open("jobman.config","r")
if fil_conf:
    for line in fil_conf:
        lst_keyval = [strng.strip() for strng in line.strip().split("#",1)[0].split(" ",1)[:2] if strng!='']
        if len(lst_keyval)==2:
            dic_config[lst_keyval[0].lower()] = lst_keyval[1]

if 'myworkdir' in dic_config.keys():
    clear_dir(dic_config['myworkdir'])
    str_dir_a = str_master_dir+delim_dir+"Available"
    if os.path.exists(str_dir_a):
        bol_more_left = True
        while bol_more_left:
            lst_a = list()
            for file in os.listdir(str_dir_a):
                lst_a.append(file)
            if len(lst_a) > 0:
                str_job = random.choice(lst_a)
                # We have a job to do...
                str_dir_b = str_master_dir+delim_dir+"Busy"
                if os.path.exists(str_dir_b):
                    shutil.move(str_dir_a+delim_dir+str_job, str_dir_b+delim_dir+str_job)
                    shutil.copyfile(str_dir_b+delim_dir+str_job, dic_config['myworkdir']+delim_dir+str_job)
                    # We now run the job from 'myworkdir'...

                    bol_more_left = False # lus
                else:
                    print "Error - Can't find 'Busy' dir: {}".format(str_dir_b)
                    sys.exit(998)
            else:
                bol_more_left = False
                print "No more jobs found in {}".format(str_dir_a)
    else:
        print "Error - Can't find 'Available' dir: {}".format(str_dir_a)
        sys.exit(999)

print "Done..."