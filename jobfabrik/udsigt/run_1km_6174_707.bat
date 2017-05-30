
:: create work dir
RMDIR /S /Q workdir_1km_6174_707
MKDIR workdir_1km_6174_707
CD workdir_1km_6174_707

:: set GDAL parameters
SET GDAL_CACHEMAX=1600
rem GDAL_SWATH_SIZE=?

:: extract 1km2 of UdgangsObj for Udsigt to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" 1km_6174_707_udgobj.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT dar_id, z, geom FROM k.pgv_udsigtudg_parcel WHERE dar_ddkn_km1 = '1km_6174_707'"

:: extract 1km2 + 2km buffer of DTM to .tiff
gdalwarp -overwrite -te 705000 6172000 710000 6177000: Y:\DSM40\DSM_40_18052017.vrt 1km_6174_707_dhmdsm.tif

:: extract 1km2 + 2km buffer of Coast line to .shp file
ogr2ogr -overwrite -f "ESRI Shapefile" -spat 705000 6172000 710000 6177000 1km_6174_707_coastl.shp PG:"host=c1503681 port=5433 user=reader dbname=pgv_2017 password=hejskat" -sql "SELECT kystlinje_id, geom FROM k.kystlinje"

:: extract 1km2 + 2km buffer of Lake shore to .shp file
:: extract 1km2 + 2km buffer of Internal walls to .shp file

:: run a septi_view on general view to output a
rem septima_view.exe general --idatt dar_id --z pgv_uo_z 1km_6174_707_dhmdsm.tif Q:\udsigt_parallel\10km_604_68\uo_1km_6040_680.shp Q:\udsigt_parallel\10km_604_68\gen_1km_6040_680.csv

:: run a septi_view on sea view to output b
rem septima_view.exe sea --idatt dar_id --z pgv_uo_z 1km_6174_707_dhmdsm.tif Q:\udsigt_parallel\10km_604_68\uo_1km_6040_680.shp Q:\udsigt_parallel\10km_604_68\cl_1km_6040_680.shp Q:\udsigt_parallel\10km_604_68\sea_1km_6040_680.csv

:: run a septi_view on lake view to output c
:: delete the input .shp and .tiff files
:: move 3x output + 3x septi_view.log to a safe place
:: complete a jobman_cell_xxx.log 

:: return to strat dir
cd ..


