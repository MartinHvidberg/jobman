import os
from osgeo import ogr

str_root_dir = r"R:\udsigt_resultat"

def count_records_in_shape(str_in_fn):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    dataSource = driver.Open(str_in_fn, 0) # 0 means read-only. 1 means writeable.
    # Check to see if shapefile is found.
    if dataSource is None:
        print 'Could not open %s' % (str_in_fn)
        return 0
    else:
        #print 'Opened %s' % (str_in_fn)
        layer = dataSource.GetLayer()
        featureCount = layer.GetFeatureCount()
        #print "Number of features in %s: %d" % (os.path.basename(str_in_fn),featureCount)
        return featureCount
    
def filename2cellname(str_in_fn):
    end = str_in_fn.rfind(".")
    beg = str_in_fn.rfind("km")
    #print "clipper : ", str_in_fn, "(", beg, end, ")", str_in_fn[beg:end]
    return str_in_fn[beg:end]
    
str_log_fn = str_root_dir+"\\"+"check_if_10k_cells_are_done_.log"
fil_log = open(str_log_fn,"w")
print "Writing output to log file: {}".format(str_log_fn)
    
for str_dir in os.listdir(str_root_dir):
    str_full_path = str_root_dir+"\\"+str_dir
    if os.path.isdir(str_full_path):# and str_dir == "10km_605_69":                           ### <--- lus
        dic_cnt = dict()
        str_log = "{} *** Checking dir: {}".format(str_dir, str_full_path)
        fil_log.write(str_log+"\n")
        print str_log
        for str_fn in os.listdir(str_full_path):
            str_cellname = filename2cellname(str_fn)
            if not str_cellname in dic_cnt.keys():
                dic_cnt[str_cellname] = {'UO':0, "Gn":0, "Se":0}
            if str_fn.endswith(".shp"):
                str_full_fn = str_full_path+"\\"+str_fn
                if str_fn.startswith("uo_"):
                    ##print "  found uo_*:", str_full_fn
                    num_cnt_uo = count_records_in_shape(str_full_fn)
                    dic_cnt[str_cellname]["UO"] = num_cnt_uo
                    ##print "    UO:", str_full_fn, "Cnt:", num_cnt_uo
                else:
                    pass# print "  Skippeng unexpected start in .shp filename:", str_full_fn
            elif str_fn.endswith(".csv"):
                str_full_fn = str_full_path+"\\"+str_fn
                if str_fn.startswith("gen"):
                    ##print "  found gen*:", str_full_fn
                    num_cnt_gn = sum(1 for line in open(str_full_fn, 'r'))
                    dic_cnt[str_cellname]["Gn"] = num_cnt_gn
                    ##print "    Gn:", str_full_fn, "Cnt:", num_cnt_gn
                elif str_fn.startswith("sea"):
                    ##print "  found sea*:", str_full_fn
                    num_cnt_se = sum(1 for line in open(str_full_fn, 'r'))
                    dic_cnt[str_cellname]["Se"] = num_cnt_se
                    ##print "    Se:", str_full_fn, "Cnt:", num_cnt_se
                else:
                    pass#print "  Skippeng unexpected start in .csv filename:", str_full_fn
            else:
                pass#print "  Skippeng unexpected extention:", str_fn

        ##print " ** Results"
        lst_keys = dic_cnt.keys()
        lst_keys.sort()
        cnt_error = 0
        for key_n in lst_keys:
            #print key_n, dic_cnt[key_n]
            if (dic_cnt[key_n]["UO"] != dic_cnt[key_n]["Gn"]) or (dic_cnt[key_n]["UO"] != dic_cnt[key_n]["Se"]):
                str_log = "            !!! - Error - not same cnt (UO, Gn, Se) in: {} = ({}, {}, {})".format(key_n, dic_cnt[key_n]["UO"], dic_cnt[key_n]["Gn"], dic_cnt[key_n]["Se"])
                fil_log.write(str_log+"\n")
                print str_log
                cnt_error += 1
            else:
                pass#print ".",
        
        str_log =  "{} ** Done with dir: {} found {} errors".format(str_dir, str_full_path, cnt_error)
        fil_log.write(str_log+"\n")
        print str_log
      
fil_log.close()
print "Done..."
print "Writing output to log file: {}".format(str_log_fn)