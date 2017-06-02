
:: create work dir
IF EXIST workdir_1km_6150_513 (
DEL /F /S /  workdir_1km_6150_513
RMDIR /S /Q workdir_1km_6150_513 )
MKDIRworkdir_1km_6150_513
CD workdir_1km_6150_513

:: start log file
echo log file for 1km_6150_513 > 1km_6150_513_cell.log
date / t >> 1km_6150_513_cell.log
time / t >> 1km_6150_513_cell.log
echo Start >> 1km_6150_513_cell.log

:: set GDAL parameters
SET GDAL_CACHEMAX=1600
rem GDAL_SWATH_SIZE=?

:: extract 1km2 of UdgangsObj for Udsigt to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" 1km_6150_513_udgobj.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT dar_id, z, geom FROM k.pgv_udsigtudg_parcel WHERE dar_ddkn_km1 = '1km_6150_513'"

:: extract 1km2 + 2km buffer of DTM to .tiff
gdalwarp -overwrite -te 511000 6148000 516000 6153000 \\C1503681\pgv2_E\DSM40\DSM_40_18052017.vrt 1km_6150_513_dhmdsm.tif

:: extract 1km2 + 2km buffer of Coast line to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" 1km_6150_513_coastl.shp -spat 511000 6148000 516000 6153000 PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT kystlinje_id as id, geom FROM k.kystlinje"

:: extract 1km2 + 2km buffer of Lake shore to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" 1km_6150_513_lakesh.shp -spat 511000 6148000 516000 6153000 PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT soe_id as id, geom FROM k.soeudsigt"

:: run a septi_view on general view to output a
call ..\..\..\Executables\septima_view_v0.0.3.exe general --idatt dar_id --zatt z 1km_6150_513_dhmdsm.tif 1km_6150_513_udgobj.shp 1km_6150_513_gen.csv
