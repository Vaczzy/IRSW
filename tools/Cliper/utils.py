import sys
from osgeo import gdal
from osgeo import ogr
import os

def IfFileExists(path):
    if not os.path.exists(path):
        print("Can not find {}.".format(path))
        sys.exit(1)

def ReadGdalDataset(srcDataPath):
    IfFileExists(srcDataPath)
    pData =gdal.Open(srcDataPath)
    if pData==None:
        print( "Failed to open {}.".format(srcDataPath))
        sys.exit(1)
    return pData


def ReadShpDataset(shppath):
    IfFileExists(shppath)
    ds = ogr.Open(shppath,True)
    if ds==None:
        print("Failed to open {}.".format(shppath))
        sys.exit(1)
    return ds

def Shp2Raster(destPath, shp, width, height, geotrans, projection):
    destDS = gdal.GetDriverByName("MEM").Create('', width, height,1, gdal.GDT_Byte) #.gdla.D. .nt16
    destDS.SetGeoTransform(geotrans)
    destDS.SetProjection(projection)
    err =gdal.RasterizeLayer(destDS,[1],shp)
    gdal.GetDriverByName("GTiff").CreateCopy(destPath, destDS)
    del destDS