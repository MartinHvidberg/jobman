# !/usr/bin/python
# -*- coding: UTF-8 -*-

# Build 20170614

import sys
import os
import datetime


"""
OVERALL IDEA
"""


def log(str_text, level, file=""):
    """ CRITICAL 50, ERROR 40, WARNING 30, INFO 20, DEBUG 10, NOTSET 0 """
    str_log = "LOG [" + str(level) + "] " + str(datetime.datetime.now()) + " : " + str_text
    if file != "":
        file.write(str_log + "\n")
    print str_log

def build_all_jobs(lst_all_cells, str_main_workdir):
    for str_cell_name in lst_all_cells:
        log("Running cell: {}".format(str_cell_name), 20)

        # Open new .bat file
        str_batch_fn = str_main_workdir + "\\haeldning_run_" + str_cell_name + ".bat"
        with open(str_batch_fn, "w") as fil_batch:
            # create work dir
            str_injob_work_dir = "workdir_" + str_cell_name
            fil_batch.write("\n:: create work dir\n")
            fil_batch.write("IF EXIST {} (\n".format(str_injob_work_dir))
            fil_batch.write("DEL /F /S /  {}\n".format(str_injob_work_dir))
            fil_batch.write("RMDIR /S /Q {} )\n".format(str_injob_work_dir))
            fil_batch.write("MKDIR {}\n".format(str_injob_work_dir))
            fil_batch.write("CD {}\n".format(str_injob_work_dir))

            # start log file
            str_injob_logfile_name = str_cell_name + "_cell.log"
            fil_batch.write("\n:: start log file\n")
            fil_batch.write("echo log file for {} > {}\n".format(str_cell_name, str_injob_logfile_name))
            fil_batch.write("date /t >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("time /t >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("echo Start >> {}\n".format(str_injob_logfile_name))

            # set GDAL parameters
            fil_batch.write("\n:: set GDAL parameters\n")
            fil_batch.write("SET GDAL_CACHEMAX=1600\n")

            # run ...
            fil_batch.write("\n:: Main run\n")
            fil_batch.write("python ..\..\..\Executables\demstat.py --dkncell {}\n".format(str_cell_name))

            # finish log file
            fil_batch.write("\necho Done... >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("date /t >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("time /t >> {}\n".format(str_injob_logfile_name))

            # move the results and log to safety
            fil_batch.write("\nmove /Y C:\\temp\\sloasp\\{}.ecr {} \n".format(str_cell_name, str_safety))
            fil_batch.write("\nmove /Y C:\\temp\\sloasp\\{}.ecl {} \n".format(str_cell_name, str_safety))

            # copy the batch run's .log file to safety
            fil_batch.write("\nmove /Y {} {} \n".format(str_injob_logfile_name, str_safety))

            fil_batch.write("\nCD .." + "\n")

            fil_batch.flush()


if __name__ == "__main__":

    #str_fn_cell_list_1km = "dkn1km_paa_land_lables.scsv"
    str_fn_cell_list_1km = "dkn1km_paa_land_lables.scsv"
    str_main_workdir = r"F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\jobman_master_sloasp\Available"  # Where the job-files go
    str_safety = r"F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\jobman_master_SloAsp\ResultReturn"  # A hardcoded place where important results are copied for safe keeping

    # open log file
    fil_log = open("make_sloasp_run.log", "w")
    log("Init", 10, fil_log)

    try:
        with open(str_fn_cell_list_1km) as f:
            lst_all_cells = [x.strip() for x in f.readlines()]
    except:
        log("ERROR - Can't open: List of cells: " + str(str_fn_cell_list_1km), 50)
        sys.exit(999)

    # ** Begin build
    log("All good to go...", 20)
    build_all_jobs(lst_all_cells, str_main_workdir)

    log("Python script {} completed sucessfuly...".format(sys.argv[0]), 20)

