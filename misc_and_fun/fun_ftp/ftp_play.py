import ftplib

import ecpass

# ecpass
dic_pass = ecpass.ecp('.ecpass')
print(dic_pass.keys())
conn = 1
host = dic_pass[conn]['host']
user = dic_pass[conn]['user']
pasw = dic_pass[conn]['pass']

# ftp
ftp = ftplib.FTP(host)
ftp.login(user, pasw)

data = []
ftp.dir(data.append)
ftp.quit()
for line in data:
    print ">", line
