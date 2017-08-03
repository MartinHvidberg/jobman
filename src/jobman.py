
# import from The Python Standard Library
import os
import sys
import logging
import shutil
import random
import datetime
import time
import subprocess
import yaml
# import from 3'rd party
# import home grown...

""" Job Man
Plan:
    Read .config file

    Delete all local files, i.e empty local work-directory
    Look through /Available and pick a job
    Move that job file to /Busy
    Make a copy of it to local work-directory
    Execute the file locally
    If exist success.jobman in local dir, then
        move job file from /Busy to /Completed, else
        move job tile from /Busy to /Discarded
    Delete all local files, i.e empty local work-directory
    
History
  ver 1.0.4 - introducing jobman_pilot.yaml as keypress seems to be difficult to handle

ToDo
    * When job pool is empty, wait for busy jobs to complete (seems to have been fixed?)
    * Send .jmlog to L rather than t C/D
    * make 'hammer time' floating, to better ensure 100% cpu use
    * re-read config at intervals
    * have jobman react to keypress, e.g. - Seems to be difficult in Python
        h  = Help "display list of keypress options, and continue"
        v  = Version "type JobMan version, and continue"
        s  = Status "type some status info, and continue"
        c' = Config "Re-read the config file"
        +  = increase "+1 on number of processes"
        -  = decrease "-1 on number of processes"
        q' = Quit "don't take new jobs, and stop when done"
        (') meanwhile substituted by the jobman_pilot.yaml
    * Change jobman.config to yaml format
"""

__version__ = "1.0.5"
__build__ = "2017-08-03ff"


def print_and_log(str_message, level='Info'):
    print str_message
    if level.lower() == 'info':
        logging.info(str_message)
    elif level.lower() == 'warning':
        logging.warning(str_message)
    elif level.lower() == 'debug':
        logging.debug(str_message)
    else:
        print "Error - print_and_log() encountered unknown error level: {}".format(level)


def read_config_file(str_fn):
    dic_conf_l = dict()
    fil_conf = open(str_fn, "r")
    if fil_conf:
        for line in fil_conf:
            lst_keyval = [strng.strip() for strng in line.strip().split("#", 1)[0].split(" ", 1)[:2] if strng != '']
            if len(lst_keyval) == 2:
                dic_conf_l[lst_keyval[0].lower()] = lst_keyval[1]
    return dic_conf_l


def read_pilot_file(str_fn, dic_conf_l):
    jm_quit_l = False  # Default quit to False, for smooth except return
    with open(str_fn, 'r') as fil:
        try:
            dic_conf_n = yaml.load(fil)
        except yaml.YAMLError as exc:
            print(exc)
            return jm_quit_l, dic_conf_l  # return most harmless
    if 'c' in dic_conf_n.keys():  # Re-read Config file
        if dic_conf_n['c'] is True:
            dic_conf_c = read_config_file(jm_config_file)
            for k in dic_conf_c.keys():  # only replace keys found in file
                dic_conf_l[k] = dic_conf_c[k]
    if 'q' in dic_conf_n.keys():  # Quit JobMan
        if dic_conf_n['q'] is True:
            jm_quit_l = True
    return jm_quit_l, dic_conf_l


def check_write_access(str_dir):
    str_test_dir_name = "delete_this_test_dir_if_it_exist_for_more_than_a_few_seconds"
    try:
        os.makedirs(str_dir + str_osep + str_test_dir_name)
        if os.path.exists(str_dir + str_osep + str_test_dir_name):
            shutil.rmtree(str_dir + str_osep + str_test_dir_name)
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


def handle_completed_processes(dic_p):
    lst_completed_processes = list() # list to collect them...
    for proc_key_i in dic_p.keys():
        dic_proc_i = dic_p[proc_key_i]
        proc = dic_proc_i['subpro']
        poll_n = proc.poll()
        if poll_n is not None:  # it's completed, i.e. stopped running
            # stop the timer
            dic_proc_i['tim_stop'] = datetime.datetime.now()
            dic_proc_i['tim_dura'] = str(dic_proc_i['tim_stop']-dic_proc_i['tim_start'])
            # write a log file
            fil_jmlog = open(dic_proc_i['workdir']+str_osep+dic_proc_i['name']+".jmlog","w")
            for itms in sorted(dic_proc_i.keys()):
                str_logline = "   $ {} : {}".format(itms, dic_proc_i[itms])
                fil_jmlog.write(str_logline+"\n")
                print str_logline
            fil_jmlog.close()

            # XXX Consider moving this block about 8 lines up, and include the include it in the logging ;-)
            # check for success
            if poll_n == 0:  # it has completed successfully
                print "Proc comp. succ. {}".format(dic_proc_i['name'])
                str_dest_dir = str_dir_c
            else:  # it has completed with error
                print "Proc comp. FAIL. {}".format(dic_proc_i['name'])
                str_dest_dir = str_dir_d
            # return all the files to /Master and clean up
            try:
                shutil.move(dic_proc_i['workdir'],str_dest_dir)
            except:
                print "Error - Can't move workdir back to master"
                sys.exit(994)
            # Remove the job from /Busy
            try:
                shutil.move(str_dir_b+str_osep+dic_proc_i['name']+".bat",str_dest_dir)
            except:
                print "Error - Can't move Busy to Complete/Discarded: {} >> {}".format(str_dir_b+str_osep+dic_proc_i['name'],str_dest_dir)
                sys.exit(993)

            # Mark process to be removed
            lst_completed_processes.append(proc_key_i)
    for compproc in lst_completed_processes:
        dic_p.pop(compproc)
    return dic_p


def saferun_subprocess(str_args, str_workwork_dir):
    try:
        process = subprocess.Popen(str_args, shell=True, cwd=str_workwork_dir)  # XXX redirect stdout= to an existing file object
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
            shutil.move(str_dir_a + str_osep + str_job, str_dir_b + str_osep + str_job)
        except:
            print "... but I wasn't fast enough."
            str_job = None  # If unsuccessful the file may have been snatch by another worker, milli-seconds before us.
            return bol_more_left, dic_p
        # make and fill work-dir in work-dir
        str_shortname = str_job.split(".", 1)[0]  # i.e. loose the file extension
        str_work_dir = dic_conf['myworkdir']
        str_workwork_dir = str_work_dir + str_osep + str_shortname
        os.makedirs(str_workwork_dir)
        try:
            shutil.copyfile(str_dir_b + str_osep + str_job, str_workwork_dir + str_osep + str_job)
        except:
            print "Error - Can't copy job file: {} Busy: {} Workdir: {}".format(str_job, str_dir_d, str_workwork_dir)
            sys.exit(996)
        # Run...
        if str_job:
            str_args = str_workwork_dir + str_osep + str_job
            safe_proc = saferun_subprocess(str_args, str_workwork_dir)
            if safe_proc:
                tim_start = datetime.datetime.now()
                dic_job = dict()
                dic_job['name'] = str_shortname
                dic_job['args'] = str_args
                dic_job['subpro'] = safe_proc
                dic_job['workdir'] = str_workwork_dir
                dic_job['tim_start'] = tim_start
                dic_job['worker_name'] = str_worker_name
                dic_job['worker_comp'] = str_worker_comp
                dic_p[str_shortname] = dic_job  # add the new job to the pool
    else:
        bol_more_left = False
    return bol_more_left, dic_p


if __name__ == "__main__":

    # Hardcoded parameters - could potentially be command line input
    jm_session_log = "jobman.sessionlog"
    jm_config_file = "jobman.config"
    jm_pilot_file = "jobman_pilot.yaml"

    # Open a session log file
    logging.basicConfig(filename=jm_session_log, level=logging.DEBUG)
    print_and_log("JobMan ver.{} - starting logfile...\n".format(__version__), "info")

    # Check if we are on windows or Linux
    if os.name.lower() in ('unix', 'posix'):
        str_osep = "/"
        #str_pyth = "python"
        #str_oext = ".sh"
    elif os.name.lower() in ('win','nt'):
        str_osep = "\\"
        #str_pyth = "C:\Python27\python.exe"
        #str_oext = ".bat"
    else:
        print "Can't understand OS named: {}".format(os.name)
        exit(993)
        print_and_log(" + OS identified...", "info")

    # Read the .config file
    str_config_fn = jm_config_file
    dic_conf = read_config_file(str_config_fn)
    print_and_log(" + Read config file: {}".format(str_config_fn), "info")

    # Note workers name and computer
    if 'name' in dic_conf.keys():
        str_worker_name = dic_conf['name']
    else:
        print "Error - .config file don't specify a name"
        sys.exit(996)
    print_and_log(" + Name of user: {}".format(str_worker_name), "info")

    if 'computer' in dic_conf.keys():
        str_worker_comp = dic_conf['computer']
        if str_worker_comp == 'GE400':
            print "I'm sorry {}, I'm afraid I can't do that. I'm not a General Electric 400-series computer.".format(dic_conf['name'])
            print "Please check if you have edited your local copy of jobman.config to reflect your actual computer."
            sys.exit(994)
    else:
        print "Error - .config file don't specify a computer"
        sys.exit(995)
    print_and_log(" + Name of computer: {}".format(str_worker_comp), "info")

    # Check, and clear, the local workdir
    if 'myworkdir' in dic_conf.keys():
        str_workdir = dic_conf['myworkdir']
        if check_write_access(str_workdir):
            clear_dir(str_workdir)
        else:
            print "Error - I can't write files to the specified work directory: {}".format(str_workdir)
            sys.exit(992)
    else:
        print "Error - The .config file contains no valid 'myworkdir'..."
        sys.exit(999)
    print_and_log(" + Work dir cleared: {}".format(str_workdir), "info")

    # Master work directory
    if 'jmjqmdir' in dic_conf.keys():
        str_master_dir = dic_conf['jmjqmdir']
    else:
        print "Error - .config file don't specify a jmjqmdir"
        sys.exit(997)
    # Check that Master directory contains directories A, B, C, D, E and L
    str_dir_a = str_master_dir + str_osep + "Available"
    str_dir_b = str_master_dir + str_osep + "Busy"
    str_dir_c = str_master_dir + str_osep + "Completed"
    str_dir_d = str_master_dir + str_osep + "Discarded"
    str_dir_e = str_master_dir + str_osep + "Executables"
    str_dir_l = str_master_dir + str_osep + "Logging"
    if not all([os.path.exists(str_dir_a),
                os.path.exists(str_dir_b),
                os.path.exists(str_dir_c),
                os.path.exists(str_dir_d),
                os.path.exists(str_dir_e),
                os.path.exists(str_dir_l)]):
        print "Error - One or more of the expected directories A, B, C, D, E, and L are missing from {}".format(str_master_dir)
        sys.exit(999)
    print_and_log(" + Master dir found: {}".format(str_master_dir), "info")

    # Assume one process at the time, if not set otherwise in .config file
    if 'max_threads' in dic_conf.keys():
        try:
            num_max_pr = int(dic_conf['max_threads'])
        except ValueError:
            num_max_pr = 1
    else:
        num_max_pr = 1
    print_and_log(" + Prepared max threads: {}".format(num_max_pr), "info")

    # Minimum time to wait between checking for a vacant process slot
    num_htime = 10 # Default 'hammer-time' to 10 sec.
    if 'hammertime' in dic_conf.keys():
        try:
            num_htime = int(dic_conf['hammertime'])
        except ValueError:
            print "Warning - .config file holds non integer value for 'hammertime'"
            # fall back on default value above...
    else:
        print "Error - .config file don't specify a hammertime"
        sys.exit(992)
    print_and_log(" + Hammer time set to: {} seconds".format(num_htime), "info")

    # All is Green - We are Good-to-go...
    print_and_log("All is Green - We are Good-to-go...\n", "info")

    # Start running processes
    bol_more_left = True  # Just assume that /Available is non-empty, we will check later.
    dic_pro = dict()  # Dictionary holding the process-objects
    jm_quit = False  # If this becomes True JobMan will finish current jobs and then quit

    while bol_more_left or len(dic_pro)>0:  # more left or more busy

        # Check on running jobs
        dic_pro = handle_completed_processes(dic_pro)
        while len(dic_pro) >= num_max_pr:  # if all slots are occupied, wait a second
            print "All processes running: {} of {}. JobMan sleeping for {} seconds".format(len(dic_pro), num_max_pr, num_htime)
            time.sleep(num_htime)  # in seconds...

        # Start up new jobs
        if bol_more_left and not jm_quit:
            # Start a new thread.
            print "Not all processes are running: {} of {}. Trying to start new...".format(len(dic_pro), num_max_pr)
            bol_more_left, dic_pro = start_new_process(dic_pro)
        ##if len(dic_pro)>0:  # Still more busy - XXX this may not be needed after bol_more_busy was replaced by len(dic_pro)>0
        ##    dic_pro = handle_completed_processes(dic_pro)  # Nessisary to process last jobs, after pool is empty

        # Look for keypressed, and write status, and maybe handle different keypress?
        # Alternative to keypress - scan a pilot-file.
        jm_quit, dic_conf = read_pilot_file(jm_pilot_file, dic_conf)

    print_and_log("\nJobMan complete...", "info")
