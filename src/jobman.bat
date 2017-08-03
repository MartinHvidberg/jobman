:: Refresh files from template
xcopy F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\jobman_udsi_client_template\jobman.bat /V /Y
xcopy F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\jobman_udsi_client_template\jobman.py /V /Y
xcopy F:\PGV\Projektarbejdsmapper\P4\Software\JobMan\jobman_udsi_client_template\Executables\*.* .\Executables /S /V /Y

:: Run
C:\Python27\python.exe jobman.py