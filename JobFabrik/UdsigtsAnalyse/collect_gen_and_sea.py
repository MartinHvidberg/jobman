import os

str_root_dir = r"R:\udsigt_resultat"
str_gen_file = str_root_dir + "\\" + "gen_collected.csv"
str_sea_file = str_root_dir + "\\" + "sea_collected.csv"
fil_gen = open(str_gen_file,"w")
fil_sea = open(str_sea_file,"w")
  
for str_dir in os.listdir(str_root_dir):
    str_full_path = str_root_dir+"\\"+str_dir
    if os.path.isdir(str_full_path):# and str_dir == "10km_610_71":                           ### <--- lus
        print str_dir, "+++"
        for str_sub_dir in os.listdir(str_full_path):
            if str_sub_dir.endswith(".csv"):
                str_full_subpath = str_full_path+"\\"+str_sub_dir
                if str_sub_dir.startswith("gen"):
                    ##print "  Open:", str_full_subpath
                    with open(str_full_subpath) as f:
                        fil_gen.writelines(f.readlines()) 
                elif str_sub_dir.startswith("sea"):
                    ##print "  Open:", str_full_subpath
                    with open(str_full_subpath) as f:
                        fil_sea.writelines(f.readlines())
                else:
                    print "  Skippeng unexpected start in .csv filename:", str_full_subpath
                pass#print "        "+str_full_subpath, num_gen, num_sea
            else:
                pass#print "  Skippeng unexpected extention:", str_sub_dir
fil_gen.close()
fil_sea.close()
 
## Check for duplicates
with open(str_gen_file,"r") as f:
    lst_lines = f.readlines()
num_len1 = len(lst_lines)
print "gen lines:", num_len1
lst_lines = list(set(lst_lines))
lst_lines.sort()
num_len2 = len(lst_lines)
print "gen lines cleaned:", num_len2
if num_len1 == num_len2:
    print "All is unique."
else:
    if True:
        print " Looking for same UO, but differen gen or sea:"
        uo_latest = ""
        for lin in lst_lines:
            lst_lin = lin.split(";")
            if lst_lin[0] == uo_latest:
                print "  r: "+uo_latest+" != "+lst_lin[1]
            else:
                uo_latest = lst_lin[0]
    if False: # Actually find the duplicates !!! SLOW                          ### <--- lus
        print " Duplicates exist. Counting ..."
        dic_cnt = dict()
        cnt_lines = 0
        for lin_f in lst_lines:
            cnt_lines += 1
            if cnt_lines % 1000 == 0:
                print str(cnt_lines) + " of " + str(num_len1)
            if lin_f in dic_cnt.keys():
                dic_cnt[lin_f] = dic_cnt[lin_f] + 1
            else:
                dic_cnt[lin_f] = 1
        lst_keys = dic_cnt.keys()
        lst_keys.sort()
        for key_f in lst_keys:
            if dic_cnt[key_f] > 1:
                print " ** " + key_f + " Count: " + dic_cnt[key_f]
     
with open(str_sea_file,"r") as f:
    lst_lines = f.readlines()
num_len1 = len(lst_lines)
print "sea lines:", len(lst_lines)
lst_lines = list(set(lst_lines))
lst_lines.sort()
num_len2 = len(lst_lines)
print "sea lines cleaned:", len(lst_lines)
if num_len1 == num_len2:
    print "All is unique."
else:
    if True:
        print " Looking for same UO, but differen gen or sea:"
        uo_latest = ""
        for lin in lst_lines:
            lst_lin = lin.split(";")
            if lst_lin[0] == uo_latest:
                print "  r: "+uo_latest+" != "+lst_lin[1]
            else:
                uo_latest = lst_lin[0]
     

print "Done..."

# *** End of Script ***

# Music that accompanied the coding of this script:
#   Prince - 1999.
