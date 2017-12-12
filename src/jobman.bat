
:: Refresh files from template
::xcopy F:\PGV\Projektarbejdsmapper\P4\Software_og_IT\JobMan\jobman_sloasp_master\jobman.py /V /Y
::xcopy F:\PGV\Projektarbejdsmapper\P4\Software_og_IT\JobMan\jobman_sloasp_master\Executables\*.* .\Executables /S /V /Y

:: Refresh files from GIT
xcopy C:\Martin\Work_GitHub\jobman\src\jobman.py /V /Y
xcopy C:\Martin\Work_GitHub\PGV4\2018_test\6_pgv_gv\beliggenhed\haeldning\demstat.py .\Executables /S /V /Y
xcopy C:\Martin\Work_GitHub\PGV4\2018_test\6_pgv_gv\beliggenhed\haeldning\demstat_helpers.py .\Executables /S /V /Y

:: Run
python jobman.py