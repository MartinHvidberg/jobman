import os
import subprocess

str_root_dir = r"R:\udsigt_resultat"

for str_dir in os.listdir(str_root_dir):
    str_full_path =str_root_dir+"\\"+str_dir
    if os.path.isdir(str_full_path):
        print str_dir, "+++"
        # ** UO
        str_cmd =r"C:\APPS\SYS\7za920\7za.exe a -y {0}\uo-{1}.7za {0}\uo_*.*".format(str_full_path, str_dir)
        print str_cmd
        str_cmd_res = os.system(str_cmd)
        print "zip result", str(type(str_cmd_res)), str_cmd_res
        if str_cmd_res == 0:
            str_cmd =r"del {0}\uo_*.*".format(str_full_path, str_dir)
            print str_cmd
            str_cmd_res = os.system(str_cmd)
            print "del result", str(type(str_cmd_res)), str_cmd_res
        # ** CL
        str_cmd =r"C:\APPS\SYS\7za920\7za.exe a -y {0}\cl-{1}.7za {0}\cl_*.*".format(str_full_path, str_dir)
        print str_cmd
        str_cmd_res = os.system(str_cmd)
        print "zip result", str(type(str_cmd_res)), str_cmd_res
        if str_cmd_res == 0:
            str_cmd =r"del {0}\cl_*.*".format(str_full_path, str_dir)
            print str_cmd
            str_cmd_res = os.system(str_cmd)
            print "del result", str(type(str_cmd_res)), str_cmd_res
            
    else:
        pass#print str_dir, "IS NOT DIR"
    #for root_s, dirs_s, files_s in os_walk