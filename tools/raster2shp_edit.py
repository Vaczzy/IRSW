import os
import numpy as np
from osgeo import gdal,ogr,osr


def tif2shp(tif_path,shp_path):
    """
    .tif raster data to .shp data
    tif_path: raster data path
    shp_path: vector data path
    """
    # Read Tif Data
    raster=gdal.Open(tif_path)
    band=raster.GetRasterBand(1) # raster data
    prj=osr.SpatialReference()
    prj.ImportFromWkt(raster.GetProjection()) # projection

    # Create Vector File
    drv=ogr.GetDriverByName("ESRI Shapefile")
    if os.path.exists(shp_path):
        drv.DeleteDataSource(shp_path)
    Polygon=drv.CreateDataSource(shp_path)

    # Create Layer
    Poly_layer=Polygon.CreateLayer('面',srs=prj,geom_type=ogr.wkbMultiPolygon)
    # Create value field (base field)
    valueField=ogr.FeildDefn('value',ogr.OFTReal) 
    Poly_layer.CreateField(valueField)

    gdal.Polygonize(band,None,Poly_layer,0)

    strValue=0
    strFilter="Value='"+str(strValue)+"'"
    Poly_layer.SetAttributeFilter(strFilter) # 筛选Value=0的显示，但显然没有Value整个字段

    pFeatureDef=Poly_layer.GetLayerDefn()
    pLayerName=Poly_layer.GetName()
    pFileName="Value"
    pFieldIndex=pFeatureDef.GetFieldIndex(pFileName)
    for pFeature in Poly_layer:
        pFeatureFID=pFeature.GetFID()
        Poly_layer.DeleteFeature(int(pFeatureFID))

    # noqa:
        # Create confidence field
    confidentField=ogr.FeildDefn('confidence',ogr.OFTReal)
    confidentField.SetPrecision(8)
    Poly_layer.CreateField(confidentField)
    
    # index=pFeatureDef.GetFieldIndex('confidence')
    # oField=pFeatureDef.GetFieldDefn(index)
    # fieldName=oField.GetNameRef()
    for pFeature in Poly_layer:
        NumOfDefn = pFeature.GetFieldCount() 

        input=np.random.randint(5,10)/10 # 写入的字段
        # pFeature.SetField2(fieldName,input)
        feature.SetField(NumOfDefn-1,input)

        Poly_layer.SetFeature(feature)
        feature=None


    strSQL="REPACK"+str(Poly_layer.GetName())
    Polygon.ExcuteSQL(strSQL,None,"")
    Poly_layer=None

    Polygon.SyncToDisk()
    Polygon=None
