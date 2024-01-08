from osgeo import gdal,ogr,osr

# driver = ogr.GetDriverByName(DRIVER_SHAPE)
# shp1 = driver.Open(erased_file, gdalconst.GA_ReadOnly)

datasource = gdal.Open('C:\IRSW\无标题.zip\无标题.png')


print(datasource)