
:: Case: Vindekilde (Klitvej)

datetime.exe --rfc-822

:: create work dir
IF EXIST workdir_1km_6184_649 (
DEL /F /S /Q workdir_1km_6184_649
RMDIR /S /Q workdir_1km_6184_649
)
MKDIR workdir_1km_6184_649
CD workdir_1km_6184_649

:: start log file
ECHO log file for 1km_6184_649 > 1km_6184_649_cell.log
date /t >> 1km_6184_649_cell.log
time /t >> 1km_6184_649_cell.log
ECHO Start >> 1km_6184_649_cell.log

:: set GDAL parameters
SET GDAL_CACHEMAX=1600

:: extract 1km2 of UdgangsObj for Udsigt to a .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" 1km_6184_649_udgobj.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT dar_id, z, geom FROM k.pgv_udsigtudg_parcel WHERE dar_ddkn_km1 = '1km_6184_649'"

:: extract 1km2 + 2km buffer of DTM to .tiff
:::gdalwarp -overwrite -te 689000 6170000 694000 6175000 -dstnodata 0 D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt 1km_6184_649_dhmdsm.tif

:: extract 1km2 + 2km buffer of Coast line to a .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" -spat 647000 6182000 652000 6187000 1km_6184_649_coastl.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT kystlinje_id as id, geom FROM k.kystlinje"

:: extract 1km2 + 2km buffer of Lake shore to a .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" -spat 647000 6182000 652000 6187000 1km_6184_649_lakesh.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT soe_id as id, geom FROM k.soeudsigt"

:: extract 1km2 + 2km buffer of Internal walls to a .shp file
rem k.barriere

:: run a septi_view on general view to output a
call ..\..\..\Executables\septima_view_v0.0.3.exe general --idatt dar_id --zatt z D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt 1km_6184_649_udgobj.shp 1km_6184_649_gen.csv
IF %ERRORLEVEL% NEQ 0 EXIT %ERRORLEVEL%
ECHO 'Succes: septiview GEN' >> 1km_6184_649_cell.log

:: run a septi_view on sea view to output b
call ..\..\..\Executables\septima_view_v0.0.3.exe sea --idatt dar_id --zatt z D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt 1km_6184_649_udgobj.shp 1km_6184_649_coastl.shp 1km_6184_649_sea.csv
IF %ERRORLEVEL% NEQ 0 EXIT %ERRORLEVEL%
ECHO 'Succes: septiview SEA' >> 1km_6184_649_cell.log

:: run a septi_view on lake view to output c
call ..\..\..\Executables\septima_view_v0.0.3.exe sea --idatt dar_id --zatt z D:\scripts\udsigtsraster\DTM\udsigtsraster\buffer2m.vrt 1km_6184_649_udgobj.shp 1km_6184_649_lakesh.shp 1km_6184_649_lak.csv
IF %ERRORLEVEL% NEQ 0 EXIT %ERRORLEVEL%
ECHO 'Succes: septiview LAK' >> 1km_6184_649_cell.log

:: copy results to PostgreSQL
SET PGHOST=c1503681
SET PGPORT=5433
SET PGUSER=brian
SET PGPASSWORD=igenigen
SET PGDATABASE=pgv_2017
psql --command="\copy h.pgv_udsigtudg_udsigt_gen from 1km_6184_649_gen.csv WITH DELIMITER ';'"
IF %ERRORLEVEL% NEQ 0 EXIT %ERRORLEVEL%
ECHO 'Succes: psql' >> 1km_6184_649_cell.log

:: delete the temp .shp and .tiff files
IF NOT "%jobman_keep_temp_files%" == "true" (
  del 1km_6184_649_udgobj.* /Q /F
  del 1km_6184_649_dhmdsm.* /Q /F
  del 1km_6184_649_coastl.* /Q /F
  del 1km_6184_649_lakesh.* /Q /F
)

:: complete a jobman_cell_xxx.log
ECHO Stop >> 1km_6184_649_cell.log
date /t >> 1km_6184_649_cell.log
time /t >> 1km_6184_649_cell.log

:: return to start dir
cd ..

datetime.exe --rfc-822