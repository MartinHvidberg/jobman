move Busy\*.bat Available
move Completed\*.bat Available
rd Completed /s /q
md Completed
move Discarded\*.bat Available
rd Discarded /s /q
md Discarded
