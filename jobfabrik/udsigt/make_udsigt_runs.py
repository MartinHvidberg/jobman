
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import datetime
##import subprocess

"""
OVERALL IDEA
 
From a list of ID's of all relevant 1km cell names...
    identify NSEW
    do not execute, but make a .bat file that will execute
        extract 1km2 of UdgangsObj for Udsigt to .shp file
        extract 1km2 + 2km buffer of DTM to .tiff
        extract 1km2 + 2km buffer of Coast line to .shp file
        extract 1km2 + 2km buffer of Lake shore to .shp file
        extract 1km2 + 2km buffer of Internal walls to .shp file
        run a septi_view on general view to output a
        run a septi_view on sea view to output b
        run a septi_view on lake view to output c
        delete the input .shp and .tiff files
        move 3x output + 3x septi_view.log to a safe place
        complete a jobman_cell_xxx.log 
"""


def log(str_text,level,file=""):
    """ CRITICAL 50, ERROR 40, WARNING 30, INFO 20, DEBUG 10, NOTSET 0 """
    str_log = "LOG ["+str(level)+"] "+str(datetime.datetime.now())+" : "+str_text
    if file != "":
        file.write(str_log+"\n")
    print str_log

#Get the extent from a tile name (1km_NNNN_EEE, 10km_NNN_EE))
def tilename_to_extent(tilename,buf=0):
    lst_tokens = tilename.split("_")
    if lst_tokens[0] == "1km":
        tile_size = 1000  # 1km grid
    elif lst_tokens[0] == "10km":
        tile_size = 10000 # 10km grid
    else:
        print "Error - Unknown DKN type: " + tilename
        return (0,0,0,0)
    N,E=lst_tokens[1:3]
    N=int(N)
    E=int(E)
    xt=(E*tile_size-buf,N*tile_size-buf,(E+1)*tile_size+buf,(N+1)*tile_size+buf)
    return xt


def build_all_jobs(lst_all_cells, str_main_workdir):

    for str_cell_name in lst_all_cells:
        log("Running cell: {}".format(str_cell_name), 20)
        
        # Open new .bat file
        str_batch_fn = str_main_workdir+"\\run_uds_"+str_cell_name+".bat"
        with open(str_batch_fn, "w") as fil_batch:

            # create work dir
            str_injob_work_dir = "workdir_"+str_cell_name
            fil_batch.write("\n:: create work dir\n")
            fil_batch.write("IF EXIST {} (\n".format(str_injob_work_dir))
            fil_batch.write("DEL /F /S /  {}\n".format(str_injob_work_dir))
            fil_batch.write("RMDIR /S /Q {} )\n".format(str_injob_work_dir))
            fil_batch.write("MKDIR {}\n".format(str_injob_work_dir))
            fil_batch.write("CD {}\n".format(str_injob_work_dir))

            # start log file
            str_injob_logfile_name = str_cell_name+"_cell.log"
            fil_batch.write("\n:: start log file\n")
            fil_batch.write("echo log file for {} > {}\n".format(str_cell_name,str_injob_logfile_name))
            fil_batch.write("date /t >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("time /t >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("echo Start >> {}\n".format(str_injob_logfile_name))

            # set GDAL parameters
            fil_batch.write("\n:: set GDAL parameters\n")
            fil_batch.write("SET GDAL_CACHEMAX=1600\n")

            # calc cell extent coordinates, with and without buffer
            #lst_cell_ext_only = tilename_to_extent(str_cell_name, 0) # not used as udsigts points are selected by attribute (faster)
            lst_cell_ext_buff = tilename_to_extent(str_cell_name, num_shot_length)

            # extract 1km2 of UdgangsObj for Udsigt to .shp file
            fil_batch.write("\n:: extract 1km2 of UdgangsObj for Udsigt to .shp file\n")
            str_intro = "ogr2ogr -overwrite "
            str_targt = "-f \"ESRI Shapefile\" {}_udgobj.shp ".format(str_cell_name)
            str_sourc = "PG:\"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat\" "
            str_where = "-sql \"SELECT dar_id, z, geom FROM k.pgv_udsigtudg_parcel WHERE dar_ddkn_km1 = '{}'\"".format(str_cell_name)
            fil_batch.write(str_intro + str_targt + str_sourc + str_where+"\n")
            del str_intro, str_targt, str_sourc, str_where

            # extract 1km2 + 2km buffer of DTM to .tiff
            ##fil_batch.write("\n:: extract 1km2 + 2km buffer of DTM to .tiff\n")
            ##str_intro = "gdalwarp -overwrite "
            ##str_extnt = "-te {} {} {} {} ".format(lst_cell_ext_buff[0], lst_cell_ext_buff[1], lst_cell_ext_buff[2], lst_cell_ext_buff[3])
            ##str_targt = r"\\C1503681\pgv2_E\DSM40\DSM_40_18052017.vrt "
            ##str_sourc = "{}_dhmdsm.tif".format(str_cell_name)
            ##fil_batch.write(str_intro + str_extnt + str_targt + str_sourc+"\n")
            ##del str_intro, str_extnt, str_targt, str_sourc

            # extract 1km2 + 2km buffer of Coast line to .shp file
            fil_batch.write("\n:: extract 1km2 + 2km buffer of Coast line to .shp file\n")
            str_intro = "ogr2ogr -overwrite "
            str_targt = "-f \"ESRI Shapefile\" {}_coastl.shp ".format(str_cell_name)
            str_extnt = "-spat {} {} {} {} ".format(lst_cell_ext_buff[0], lst_cell_ext_buff[1], lst_cell_ext_buff[2], lst_cell_ext_buff[3])
            str_sourc = "PG:\"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat\" "
            str_where = "-sql \"SELECT kystlinje_id as id, geom FROM k.kystlinje\""
            fil_batch.write(str_intro + str_targt + str_extnt + str_sourc + str_where+"\n")
            del str_intro, str_targt, str_extnt, str_sourc, str_where

            # extract 1km2 + 2km buffer of Lake shore to .shp file
            fil_batch.write("\n:: extract 1km2 + 2km buffer of Lake shore to .shp file\n")
            str_intro = "ogr2ogr -overwrite "
            str_targt = "-f \"ESRI Shapefile\" {}_lakesh.shp ".format(str_cell_name)
            str_extnt = "-spat {} {} {} {} ".format(lst_cell_ext_buff[0], lst_cell_ext_buff[1], lst_cell_ext_buff[2], lst_cell_ext_buff[3])
            str_sourc = "PG:\"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat\" "
            str_where = "-sql \"SELECT soe_id as id, geom FROM k.soeudsigt\""
            fil_batch.write(str_intro + str_targt + str_extnt + str_sourc + str_where+"\n")
            del str_intro, str_targt, str_extnt, str_sourc, str_where

            # :: extract 1km2 + 2km buffer of Internal walls to .shp file
            fil_batch.write("\n:: extract 1km2 + 2km buffer of Internal walls to a .shp file\n")
            fil_batch.write("rem k.barrierecd ..\n")

            # run a septi_view on general view, and bring the results to safety
            fil_batch.write("\n:: run a septi_view on general view\n")
            str_exefil = "call ..\..\..\Executables\septima_view_v0.0.3.exe general "
            str_attrib = "--idatt dar_id --zatt z "
            str_demdsm = r"D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt "
            str_udgobj = "{}_udgobj.shp ".format(str_cell_name)
            str_outfil = "{}_gen.csv".format(str_cell_name)
            fil_batch.write(str_exefil + str_attrib + str_demdsm + str_udgobj + str_outfil +"\n")
            fil_batch.write("copy {} {} /A /V /Y \n".format(str_outfil,str_safety))
            del str_exefil, str_attrib, str_demdsm, str_udgobj, str_outfil
            fil_batch.write("IF %ERRORLEVEL% NEQ 0 ECHO %ERRORLEVEL%\n")
            fil_batch.write("ECHO 'Succes: septiview {}' >> {}_cell.log\n".format("GEN", str_cell_name))

            # run a septi_view on sea view, and bring the results to safety
            fil_batch.write("\n:: run a septi_view on general view\n")
            str_exefil = "call ..\..\..\Executables\septima_view_v0.0.3.exe sea "
            str_attrib = "--idatt dar_id --zatt z "
            str_demdsm = r"D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt "
            str_udgobj = "{}_udgobj.shp ".format(str_cell_name)
            str_coalne = "{}_coastl.shp ".format(str_cell_name)
            str_outfil = "{}_sea.csv".format(str_cell_name)
            fil_batch.write(str_exefil + str_attrib + str_demdsm + str_udgobj + str_coalne + str_outfil +"\n")
            fil_batch.write("copy {} {} /A /V /Y \n".format(str_outfil,str_safety))
            del str_exefil, str_attrib, str_demdsm, str_udgobj, str_coalne, str_outfil
            fil_batch.write("IF %ERRORLEVEL% NEQ 0 ECHO %ERRORLEVEL%\n")
            fil_batch.write("ECHO 'Succes: septiview {}' >> {}_cell.log\n".format("SEA", str_cell_name))

            # run a septi_view on lake view, and bring the results to safety
            fil_batch.write("\n:: run a septi_view on general view\n")
            str_exefil = "call ..\..\..\Executables\septima_view_v0.0.3.exe sea "
            str_attrib = "--idatt dar_id --zatt z "
            str_demdsm = r"D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt "
            str_udgobj = "{}_udgobj.shp ".format(str_cell_name)
            str_coalne = "{}_lakesh.shp ".format(str_cell_name)
            str_outfil = "{}_lak.csv".format(str_cell_name)
            fil_batch.write(str_exefil + str_attrib + str_demdsm + str_udgobj + str_coalne + str_outfil +"\n")
            fil_batch.write("copy {} {} /A /V /Y \n".format(str_outfil,str_safety))
            del str_exefil, str_attrib, str_demdsm, str_udgobj, str_coalne, str_outfil
            fil_batch.write("IF %ERRORLEVEL% NEQ 0 ECHO %ERRORLEVEL%\n")
            fil_batch.write("ECHO 'Succes: septiview {}' >> {}_cell.log\n".format("LAK", str_cell_name))


            # :: copy results to PostgreSQL
            fil_batch.write("\n:: copy results to PostgreSQL")
            fil_batch.write("SET PGHOST=c1503681\n")
            fil_batch.write("SET PGPORT=5433\n")
            fil_batch.write("SET PGUSER=brian\n")
            fil_batch.write("SET PGPASSWORD=igenigen\n")
            fil_batch.write("SET PGDATABASE=pgv_2017\n")
            fil_batch.write("psql --command=\"\\copy h.pgv_udsigtudg_udsigt_gen from {}_gen.csv WITH DELIMITER ';'\"\n".format(str_cell_name))
            fil_batch.write("psql --command=\"\\copy h.pgv_udsigtudg_udsigt_sea from {}_sea.csv WITH DELIMITER ';'\"\n".format(str_cell_name))
            fil_batch.write("psql --command=\"\\copy h.pgv_udsigtudg_udsigt_lak from {}_lak.csv WITH DELIMITER ';'\"\n".format(str_cell_name))
            fil_batch.write("IF %ERRORLEVEL% NEQ 0 ECHO %ERRORLEVEL%\n")
            fil_batch.write("ECHO 'Succes: psql' >> {}_cell.log\n".format(str_cell_name))

            # delete the temp .shp and .tiff files
            fil_batch.write("\nif not \"%jobman_keep_temp_files%\" == \"true\" (\n")
            fil_batch.write("  del {}_udgobj.* /Q /F\n".format(str_cell_name))
            fil_batch.write("  del {}_coastl.* /Q /F\n".format(str_cell_name))
            fil_batch.write("  del {}_lakesh.* /Q /F )\n".format(str_cell_name))

            # finish log file
            fil_batch.write("\necho Done... >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("date /t >> {}\n".format(str_injob_logfile_name))
            fil_batch.write("time /t >> {}\n".format(str_injob_logfile_name))

            # copy the batch run's .log file to safety
            fil_batch.write("\ncopy {} {} /A /V /Y \n".format(str_injob_logfile_name,str_safety))

            fil_batch.write("\nCD .." + "\n")

            fil_batch.flush()


if __name__=="__main__":

    ##bol_run_septiview = True # Default = True, but should be False while testing on computers not running Septi_View.exe

    num_shot_length = 2000 # SeptiView shoots 2km
    str_fn_cell_list_1km = "cell_samp_1km.txt"
    str_main_workdir = r"F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\jobman_master_udsi\Available"  # Where the job-files go
    str_main_workdir = r"R:\Martin\JobMan_work_udsi\workers"  # <-- for test
    str_safety = r"F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\Collect_sequre" # A hardcoded place where important results are copied for safe keeping

    # open log file
    fil_log = open("make_udsigt_run.log", "w")
    log("Init", 10, fil_log)

    try:
        with open(str_fn_cell_list_1km) as f:
            lst_all_cells = [x.strip() for x in f.readlines()]
    except:
        log("ERROR - Can't open: List of cells: "+str(str_fn_cell_list_1km), 50)
        sys.exit(999)
    
    # ** Begin build
    log("All good to go...",20)
    build_all_jobs(lst_all_cells, str_main_workdir)

    log("Python script {} completed sucessfuly...".format(sys.argv[0]), 20)

