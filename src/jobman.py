
# import from Standard Library
import os
import sys
import shutil
import random
import datetime
import time
import subprocess
# import from 3'rd party
# import home grown...

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


def read_config_file(str_fn):
    dic_conf = dict()
    fil_conf = open(str_fn, "r")
    if fil_conf:
        for line in fil_conf:
            lst_keyval = [strng.strip() for strng in line.strip().split("#", 1)[0].split(" ", 1)[:2] if strng != '']
            if len(lst_keyval) == 2:
                dic_conf[lst_keyval[0].lower()] = lst_keyval[1]
    return dic_conf


def check_write_access(str_dir):
    str_test_dir_name = "delete_this_test_dir_if_it_exist_for_more_than_a_few_seconds"
    try:
        os.makedirs(str_dir + delim_dir + str_test_dir_name)
        if os.path.exists(str_dir + delim_dir + str_test_dir_name):
            shutil.rmtree(str_dir + delim_dir + str_test_dir_name)
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


def handle_completed_processes(dic_p):
    lst_completed_processes = list() # list to collect them...
    for proc_key_i in dic_p.keys():
        dic_proc_i = dic_p[proc_key_i]
        proc = dic_proc_i['subpro']
        poll_n = proc.poll()
        if poll_n is not None:  # it's completed, i.e. stopped running
            if poll_n == 0:  # it has completed sucessfully
                print "Proc comp. succ. {}".format(dic_proc_i['name'])
                # XXX Handle the results of the calculations...
            else:  # it has completed with error
                print "Proc comp. FAIL. {}".format(dic_proc_i['name'])
                # XXX Handle the results of the calculations...
            # Mark process to be removed
            lst_completed_processes.append(proc_key_i)
    for compproc in lst_completed_processes:
        dic_p.pop(compproc)
    return dic_p

def saferun_subprocess(str_args, str_workwork_dir):
    try:
        process = subprocess.Popen(str_args, shell=True, cwd=str_workwork_dir)
    except OSError as e:
        print "Error - OSError says: {}".format(e.message)
        return None
    except ValueError as e:
        print "Error - ValueError says: {}".format(e.message)
        return None
    except:
        print "Error - Unknown Popen() error"
        return None
    return process

def start_new_process(dic_p):
    lst_a = list()
    for fil_a in os.listdir(str_dir_a):
        lst_a.append(fil_a)
    if len(lst_a) > 0:
        # We have a job to do...
        bol_more_left = True
        str_job = random.choice(lst_a)
        print "I picked job: {}".format(str_job)
        # Secure the file, so nobody else grabs it
        try:
            shutil.move(str_dir_a + delim_dir + str_job, str_dir_b + delim_dir + str_job)
        except:
            print "... but I wasn't fast enough."
            str_job = None  # If unsuccessful the file may have been snatch by another worker, milli-seconds before us.
            return bol_more_left, dic_p
        # make and fill work-dir in work-dir
        str_shortname = str_job.split(".", 1)[0] # i.e. loose the file extension
        str_work_dir = dic_conf['myworkdir']
        str_workwork_dir = str_work_dir + delim_dir + str_shortname
        os.makedirs(str_workwork_dir)
        try:
            shutil.copyfile(str_dir_b + delim_dir + str_job, str_workwork_dir + delim_dir + str_job)
        except:
            print "Error - Can't copy job file: {} Busy: {} Workdir: {}".format(str_job, str_dir_d, str_workwork_dir)
            sys.exit(996)
        # Run...
        if str_job:
            str_args = str_workwork_dir + delim_dir + str_job
            safe_proc = saferun_subprocess(str_args, str_workwork_dir)
            if safe_proc:
                tim_start = datetime.datetime.now()
                dic_job = dict()
                dic_job['name'] = str_shortname
                dic_job['args'] = str_args
                dic_job['subpro'] = safe_proc
                dic_job['workdir'] = str_workwork_dir
                dic_job['tim_start'] = tim_start
                dic_p[str_shortname] = dic_job # add the new job to the pool
    else:
        bol_more_left = False
    return bol_more_left, dic_p


if __name__ == "__main__":

    # Assume we are on windows
    delim_dir = "\\"

    # Read the .config file
    dic_conf = read_config_file("jobman.config")

    # Check, and clear, the 'myworkdir'
    if 'myworkdir' in dic_conf.keys():
        workdir = dic_conf['myworkdir']
        if check_write_access(workdir):
            clear_dir(workdir)
    else:
        print "Error - The .config file contains no valid 'myworkdir'..."
        sys.exit(999)

    # Master work directory
    if 'jmjqmdir' in dic_conf.keys():
        str_master_dir = dic_conf['jmjqmdir']
    else:
        print "Error - .config file don't specify a jmjqmdir"
        sys.exit(997)

    # Check directories A, B, C, D, E and L
    str_dir_a = str_master_dir + delim_dir + "Available"
    str_dir_b = str_master_dir + delim_dir + "Busy"
    str_dir_c = str_master_dir + delim_dir + "Completed"
    str_dir_d = str_master_dir + delim_dir + "Discarded"
    str_dir_e = str_master_dir + delim_dir + "Executables"
    str_dir_l = str_master_dir + delim_dir + "Logging"
    if not all([os.path.exists(str_dir_a),
                os.path.exists(str_dir_b),
                os.path.exists(str_dir_c),
                os.path.exists(str_dir_d),
                os.path.exists(str_dir_e),
                os.path.exists(str_dir_l)]):
        print "Error - One or more of the expected directories A, B, C, D, E, and L are missing..."
        sys.exit(999)

    # Assume one process at the time, if not set otherwise in .config file
    if 'max_threads' in dic_conf.keys():
        try:
            num_max_pr = int(dic_conf['max_threads'])
        except ValueError:
            num_max_pr = 1
    else:
        num_max_pr = 1

    # Minimum time to wait between checking for a vacant process slot
    num_htime = 10
    if 'hammertime' in dic_conf.keys():
        try:
            num_htime = int(dic_conf['hammertime'])
        except ValueError:
            print "Warning - .config file holds non integer value for 'hammertime'"
            # fall back on default value above...


    # All is Green - We are Good-to-go...
    print "All is Green - We are Good-to-go..."

    # Start running processes
    bol_more_left = True  # Just assume that /Available is non-empty, we will check later.
    dic_pro = dict()  # Dictionary holding the process-objects
    while bol_more_left:
        while len(dic_pro) >= num_max_pr:
            print "dic too long: {} >= {} :: {}".format(len(dic_pro),num_max_pr,dic_pro)
            time.sleep(num_htime)  # in seconds...
            print "T",
            # replace 'T' with look for keypressed, and write status, and maybe handle different keypress?
            dic_pro = handle_completed_processes(dic_pro)
        # Start a new thread.
        print "dic too short: {} < {} :: {}".format(len(dic_pro),num_max_pr,dic_pro)
        bol_more_left, dic_pro = start_new_process(dic_pro)

    print "JobMan complete..."
