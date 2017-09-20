md Workers

:: Refresh files from template
xcopy ..\jobman_master\jobman.py /V /Y
xcopy ..\jobman_master\Executables\*.* Executables\ /S /V /Y

:: Run
python jobman.py