import os
import subprocess
import time

str_root_dir = r"Q:\udsigt_parallel"

for str_dir in os.listdir(str_root_dir):
    str_full_path =str_root_dir+"\\"+str_dir
    if os.path.isdir(str_full_path): #and str_dir != "10km_604_68":
        print "\n" + str_dir, "+++"
        num_fst = 9999999999
        num_lst = 0
        for str_sub_dir in os.listdir(str_full_path):
            if str_sub_dir.endswith(".csv"):
                tim_file = os.path.getmtime(str_full_path+"\\"+str_sub_dir)
                #print "   file modified: %s" % time.ctime(os.path.getmtime(str_full_path+"\\"+str_sub_dir))
                
                if tim_file < num_fst:
                    num_fst = tim_file
                if tim_file > num_lst:
                    num_lst = tim_file
        print "   first modified: %s" % time.ctime(num_fst)
        print "   last  modified: %s" % time.ctime(num_lst)
    else:
        pass#print str_dir, "IS NOT DIR"
    #for root_s, dirs_s, files_s in os_walk