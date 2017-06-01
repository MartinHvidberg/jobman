
:: create work dir
IF EXIST workdir_1km_6172_691xxx (
DEL /F /S /Q workdir_1km_6172_691
RMDIR /S /Q workdir_1km_6172_691
) 
MKDIR workdir_1km_6172_691
CD workdir_1km_6172_691

:: set GDAL parameters
SET GDAL_CACHEMAX=1600
rem GDAL_SWATH_SIZE=?

:: extract 1km2 of UdgangsObj for Udsigt to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" 1km_6172_691_udgobj.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT dar_id, z, geom FROM k.pgv_udsigtudg_parcel WHERE dar_ddkn_km1 = '1km_6172_691'"

:: extract 1km2 + 2km buffer of DTM to .tiff
rem gdalwarp -overwrite -te 689000 6170000 694000 6175000: \\C1503681\pgv2_E\DSM40\DSM_40_18052017.vrt 1km_6172_691_dhmdsm.tif

:: extract 1km2 + 2km buffer of Coast line to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" -spat 689000 6170000 694000 6175000 1km_6172_691_coastl.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT kystlinje_id as id, geom FROM k.kystlinje"

:: extract 1km2 + 2km buffer of Lake shore to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" -spat 689000 6170000 694000 6175000 1km_6172_691_lakesh.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT soe_id as id, geom FROM k.soeudsigt"

:: extract 1km2 + 2km buffer of Internal walls to .shp file
rem k.barriere

:: run a septi_view on general view to output a
call ..\..\..\Executables\septima_view_v0.0.3.exe general --idatt dar_id --z z 1km_6172_691_dhmdsm.tif 1km_6172_691_udgobj.shp 1km_6172_691_gen.csv

:: run a septi_view on sea view to output b
rem septima_view_v0.0.3.exe sea --idatt dar_id --z z 1km_6172_691_dhmdsm.tif 1km_6172_691_udgobj.shp Q:\udsigt_parallel\10km_604_68\cl_1km_6040_680.shp Q:\udsigt_parallel\10km_604_68\sea_1km_6040_680.csv

:: run a septi_view on lake view to output c

:: delete the temp .shp and .tiff files
if not "%jobman_keep_temp_files%" == "true" (
  rem del 1km_6172_691_udgobj.* /Q /F
  rem del 1km_6172_691_dhmdsm.* /Q /F
  rem del 1km_6172_691_coastl.* /Q /F
  rem del 1km_6172_691_lakesh.* /Q /F
)

:: move 3x output + 3x septi_view.log to a safe place
:: complete a jobman_cell_xxx.log

:: return to strat dir
cd ..

goto END

:ERROR
Echo Some sort of error in this batch file...

:END