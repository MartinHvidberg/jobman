
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import datetime
import subprocess

"""
OVERALL IDEA
 
 loop over 10km griddet
   start en overprocess som omfatter 1 10km celle, lad den arbejde i 1 /sub_dir/ 
     Del data op i 100 delarealer ag 1km gridcelle stoerrelse
       For hver 1km celle
         Tilrettelaeg: udgangsopjekt.shp, DSM og gerne kyst linje
         Skriv en .bat fil
         Fyr den af!
       sikre (arkiver) in- og output data til en opsamlende folder (anden stoerre disk?)
         
Dogmer:
- Hver 1km process er selfcontained og fuldt afsluttet i en koersel. Som forhaabentligt er hurtig (max nogle timer)
- Hver 10km koerer filmaesigt isoleret i et dir (0..F).
- 16 CPU'er arbejde paa 16 samtidige 10km overprocesser
- Naar en 10km overprocess er slut gives besked i .log saa data kan manuelt kvalitetssikres, efterhaanden som de bliver faerdige
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

def list_1km_in_10km_cell(str_10km_cell_name):
    lst_tok = str_10km_cell_name.strip().strip('"').split("_")
    if len(lst_tok) == 3 and lst_tok[0] == "10km":
        lst_ret = list()
        #print str_10km_cell_name
        for i in range(10):
            for j in range(10):
                lst_ret.append("1km_"+lst_tok[1]+str(i)+"_"+lst_tok[2]+str(j))
        return lst_ret
    else:
        log("ERROR - can't make 1km celles of 10km cell: "+str(str_10km_cell_name), 40)
        return 999

def build_all_overjobs(lst_all_over_cells, str_main_workdir):
    
    def build_all_subjobs(lst_sub_cells, str_over_dir, str_dem_file):
        for sub_cell in lst_sub_cells:
            ##if not sub_cell in ["1km_6172_690","1km_6172_691","1km_6173_690","1km_6173_691"]:
            ##    continue
            log("running subcell: {}".format(sub_cell), 20, fil_over_cell_log)
            # Create copy of relevant udsigts points
            str_cmd_call = 'ogr2ogr -overwrite -f "ESRI Shapefile" {0}uo_{1}.shp PG:"host=c1400067 user=brian dbname=pgv password=igenigen" "temp.pgv_dar_x_bbr_h_ltd" -where dar_1km_grid=\'{1}\''.format(str_over_dir, sub_cell)
            log(str_cmd_call, 10)
            if not bol_uo_is_pregenerated:
                subprocess.call(str_cmd_call, shell=True)
            else:
                log(" - skipping due to: bol_uo_is_pregenerated", 10, fil_over_cell_log)
                
            # Create copy of relevant coast line
            noget = tilename_to_extent(sub_cell, num_shot_length)
            log(str_cmd_call, 10, fil_over_cell_log)
            str_coast_file = "{}cl_{}.shp".format(str_over_dir, sub_cell)
            str_cmd_call = 'ogr2ogr -overwrite -f "ESRI Shapefile" {} PG:"host=c1400067 user=brian dbname=pgv password=igenigen" "dec2016lev.pgv_kildedata_kystlinje" -clipsrc {} {} {} {}'.format(str_coast_file, noget[0], noget[1], noget[2], noget[3])
            log(str_cmd_call, 10, fil_over_cell_log)
            if not bol_cosat_is_pregenerated:
                subprocess.call(str_cmd_call, shell=True)
            else:
                log(" - skipping due to: bol_cosat_is_pregenerated", 10, fil_over_cell_log)
            
            # Name UO shp. file 
            str_uo_file = "{1}uo_{0}.shp".format(sub_cell, str_over_dir)
            str_csv_file = str_uo_file.replace(".shp",".csv")
            str_cmd_call_gen = "septima_view.exe general --idatt dar_id --zatt pgv_uo_z {} {} {}".format(str_dem_file, str_uo_file, str_csv_file.replace("uo","gen"))
            fil_batch.write(str_cmd_call_gen+"\n")
            log(str_cmd_call_gen, 10, fil_over_cell_log)
            str_cmd_call_hav = "septima_view.exe sea --idatt dar_id --zatt pgv_uo_z {} {} {} {}".format(str_dem_file, str_uo_file, str_coast_file, str_csv_file.replace("uo","sea"))
            fil_batch.write(str_cmd_call_hav+"\n")
            log(str_cmd_call_hav, 10, fil_over_cell_log)

    for over_cell in lst_all_over_cells:
        log("Running Overcell: {} in {}".format(over_cell,str_main_workdir), 20)
        fil_over_cell_log = open(str_main_workdir+"make_udsigt_run_"+over_cell+".log","w")
        log("Init", 10, fil_over_cell_log)
        
        # Open new .bat file
        str_batch_fn = str_main_workdir+"\\udsigt_run_"+over_cell+".bat"
        with open(str_batch_fn, "w") as fil_batch:
            
            fil_batch.write("SET GDAL_CACHEMAX=1600\n")
        
            # Make list of sub-cells
            lst_sub_cells = list_1km_in_10km_cell(over_cell)
            
            # Open and clear relevant sub-dir
            str_over_dir = str_main_workdir+over_cell+"\\"
            if not os.path.exists(str_over_dir):
                os.makedirs(str_over_dir)
            if len(os.listdir(str_over_dir)) != 0:
                log("ERROR - output directory is non-empty: "+str(str_over_dir), 40, fil_over_cell_log)
                log("WARNING - Skipping this cell, due to non-empty output directory: "+str(over_cell), 30, fil_over_cell_log)
                
            # Establish connection to DEM
            #str_dem_file = r"//C1503681/pgv2_Q/DSM160/DSM160.vrt"
            str_dem_file = r"F:\GDB\DHM\AnvendelseGIS\DSM_20160318.vrt"
            
            # Call relevant sub-jobs
            build_all_subjobs(lst_sub_cells, str_over_dir, str_dem_file)
            
            # Move the whole thing from Parrallell to Archive...
            # XXX TBD

if __name__=="__main__":
    
    bol_uo_is_pregenerated = True # False # Normally False, but can be True during debugging...
    bol_cosat_is_pregenerated = False # True # Normally False, but can be True during debugging...
    num_shot_length = 2000 # SeptiView shoots 2km
    
    ### Note! the +2m was added while creating temp.pgv_dar_x_bbr_h_ltd...
    #create table temp.pgv_dar_x_bbr_h_ltd as
    #  select geom, dar_id, dar_1km_grid, dar_hoejde+2
    #    from kilde.pgv_dar_x_bbr_h;
    
    # ** Check requirements
    
    # Check udsigt points exist
    
    # Check DEM exist
    
    # Check coastline exist
    
    # Check Main Workdir exist
    str_main_workdir = "Q:\\udsigt_parallel\\"
    print "MW", str_main_workdir
    
    # Check Main archive exist
    str_main_archive = "Q:\\udsigt_parallel\\udsigt_archive\\"
    
    # Check lst_all_over_cells
    str_filename_list_10km_grid = r"//C1503681/pgv2_Q/udsigt_parallel/list_10km_celler_DKnord_fra621op.txt"
    lst_all_over_cells = list()
    try:
        with open(str_filename_list_10km_grid) as f:
            lst_file_content = f.readlines()
    except:
        log("ERROR - Can't open: List of over-cells: "+str(str_filename_list_10km_grid), 50)
        sys.exit()
    lst_all_over_cells = [varx.strip().strip('"') for varx in lst_file_content]
    
    # ** Begin build
    log("All good to go...",20)
    build_all_overjobs(lst_all_over_cells, str_main_workdir)
    