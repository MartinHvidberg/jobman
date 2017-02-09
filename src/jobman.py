
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

# import from Standard Library
import os, sys
import shutil
import random
import time
import subprocess
# import from 3'rd party
# import home grown...

def read_config_file(str_fn):
    dic_config = dict()
    fil_conf = open(str_fn, "r")
    if fil_conf:
        for line in fil_conf:
            lst_keyval = [strng.strip() for strng in line.strip().split("#", 1)[0].split(" ", 1)[:2] if strng != '']
            if len(lst_keyval) == 2:
                dic_config[lst_keyval[0].lower()] = lst_keyval[1]
    return dic_config

def check_write_access(str_dir):
    str_test_dir_name = "delete_this_test_dir_if_it_exist_for_more_than_a_few_seconds"
    try:
        os.makedirs(str_dir+delim_dir+str_test_dir_name)
        if os.path.exists(str_dir+delim_dir+str_test_dir_name):
            shutil.rmtree(str_dir+delim_dir+str_test_dir_name)
            return True
    except:
        return False

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
    return

def handle_completed_processes(set_p):
    XXX.poll()
    return set_p

def start_new_process(set_p):
    lst_a = list()
    for file in os.listdir(str_dir_a):
        lst_a.append(file)
    if len(lst_a) > 0:
        # We have a job to do...
        bol_more_left = True
        str_job = random.choice(lst_a)
        print "I picked job: {}".format(str_job)
        # Secure the file, so nobody else grabs it
        try:
            shutil.move(str_dir_a + delim_dir + str_job, str_dir_b + delim_dir + str_job)
        except:
            print "... but I wan't fast enough."
            str_job = None # If unsuccessful the file may have been snatch by another worker, milli-seconds before us...
            return (bol_more_left, set_p)
        # make and fill work-dir in work-dir
        str_work_dir = dic_config['myworkdir']
        str_workwork_dir = str_work_dir + delim_dir + str_job.split("." ,1)[0]
        os.makedirs(str_workwork_dir)
        print "workwork", str_workwork_dir
        shutil.copyfile(str_dir_b + delim_dir + str_job, str_workwork_dir + delim_dir + str_job)
        # Run...
        if str_job:
            str_args = str_workwork_dir+delim_dir+str_job
            set_p.add(subprocess.Popen(str_args, shell=True, cwd=str_work_dir))
    else:
        bol_more_left = False
    return (bol_more_left, set_p)

if __name__ == "__main__":

    # Assume we are on windows
    delim_dir = "\\"

    # Master work directory XXX Should be a argv...
    str_master_dir = r"C:\Martin\Work_github\jobman\jobman_master"

    # Read the .config file
    dic_config = read_config_file("jobman.config")

    # Check, and clear, the 'myworkdir'
    if 'myworkdir' in dic_config.keys():
        workdir = dic_config['myworkdir']
        if check_write_access(workdir):
            clear_dir(workdir)
    else:
        print "Error - The .config file contains no valid 'myworkdir'..."
        sys.exit(999)

    # Check directories A, B, C, D, E and L
    str_dir_a = str_master_dir+delim_dir+"Available"
    str_dir_b = str_master_dir+delim_dir+"Busy"
    str_dir_c = str_master_dir+delim_dir+"Completed"
    str_dir_d = str_master_dir+delim_dir+"Discarded"
    str_dir_e = str_master_dir+delim_dir+"Executables"
    str_dir_l = str_master_dir+delim_dir+"Logging"
    if not all([os.path.exists(str_dir_a),
               os.path.exists(str_dir_b),
               os.path.exists(str_dir_c),
               os.path.exists(str_dir_d),
               os.path.exists(str_dir_e),
               os.path.exists(str_dir_l)]):
        print "Error - One or more of the expected directories A, B, C, D, E, and L are missing..."
        sys.exit(999)

    # Assume one process at the time, if not set otherwise in .config file
    if 'max_threads' in dic_config.keys():
        try:
            num_max_pr = int(dic_config['max_threads'])
        except:
            num_max_pr = 1
    else:
        num_max_pr = 1

    # Start running processes
    bol_more_left = True  # Just assume that /Available is non-empty, we will check later.
    num_vacant_pr = num_max_pr # No processes started, yet
    set_procs = set() # Set holding the process objects
    while bol_more_left:
        while num_vacant_pr < 1:
            print "+",
            time.sleep(1) # in seconds...
            num_vacant_pr = num_max_pr - len(handle_completed_processes(set_procs))
        # Start a new thread.
        bol_more_left, set_procs = start_new_process(set_procs)
        num_vacant_pr = num_max_pr - len(set_procs)

    print "JobMan complete..."
