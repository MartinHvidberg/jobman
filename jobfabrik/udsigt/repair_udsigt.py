
import os.path

def get_over_cell(str_cell):
    #print "  # in ", str_cell # |km_6180_718|
    toks_ut = [s[:-1] for s in str_cell.split("_")]
    return "km_"+toks_ut[1]+"_"+toks_ut[2]        
            
fn_in = r"R:\udsigt_resultat\check_if_10k_cells_are_done_.ecs"
print "Reading:", fn_in, "\n"
fn_out = fn_in.replace(".ecs",".ect")

with open(fn_in, 'r') as fil_in:
    with open(fn_out, "w") as fil_out:
        fil_out.write("SET GDAL_CACHEMAX=1600\n")
        for line in fil_in:
            # expect: km_6202_712 = (35, 17, 35)
            toks = line.replace("(","").replace(")","").split("=")
            km1_name = toks[0].strip()
            #print 
            uo, ge, se = (int(strx.strip()) for strx in toks[1].strip().split(","))
            #print ":: ; ;", km1_name, uo, ge, se
            if (uo != ge) or (uo != se):
                # Check if files are available
                km10_nam = get_over_cell(km1_name)
                str_uo_fn = r"R:\udsigt_resultat\10"+km10_nam+"\uo_1"+km1_name+".shp"
                ##print r"copy {} C:\temp\ /v".format(str_uo_fn)
                str_xx_fn = r"Q:\udsigt_parallel\lapper\xxx_1{}.csv".format(km1_name)
                if not os.path.isfile(str_uo_fn):
                    print "Can't find:", str_uo_fn
                    continue
                if uo != ge:
                    # Create new GEN batch lines
                    str_gen_fn = str_xx_fn.replace("xxx","gen")
                    str_out = r"{}; septima_view.exe general --idatt dar_id --zatt pgv_uo_z F:\GDB\DHM\AnvendelseGIS\DSM_20160318.vrt {} {}".format(str(uo),str_uo_fn,str_gen_fn)
                    fil_out.write(str_out+"\n")
                if uo != se:
                    str_cl_fn = str_uo_fn.replace("uo_","cl_")
                    str_sea_fn = str_xx_fn.replace("xxx","sea")
                    if not os.path.isfile(str_cl_fn):
                        print "Can't find:", str_cl_fn
                        continue
                    str_out = r"{}; septima_view.exe sea --idatt dar_id --zatt pgv_uo_z F:\GDB\DHM\AnvendelseGIS\DSM_20160318.vrt {} {} {}".format(str(uo),str_uo_fn,str_cl_fn,str_sea_fn)
                    fil_out.write(str_out+"\n")

print "\nDone..."