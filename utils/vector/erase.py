from osgeo import gdal,ogr,osr,gdalconst

def erase(erased_file, eraser_file, output_file, output_layer_name=""):
    """
    vector erase

    Params:
        erased_file: xxxxxxx
        eraser_file: xxxxxxx
        output_file: xxxxxxx
        output_layer_name: output layer name
    """
    driver = ogr.GetDriverByName("ESRI Shapefile")
    shp1 = driver.Open(erased_file, gdalconst.GA_ReadOnly)
    shp2 = driver.Open(eraser_file, gdalconst.GA_ReadOnly)
    src_layer1 = shp1.GetLayer()
    src_layer2 = shp2.GetLayer()
    srs1 = src_layer1.GetSpatialRef()
    srs2 = src_layer2.GetSpatialRef()
    if srs1.GetAttrValue('AUTHORITY',1) != srs2.GetAttrValue('AUTHORITY',1):
        print("空间参考不一致!")
        return
    target_ds = ogr.GetDriverByName("ESRI Shapefile").CreateDataSource(output_file)
    target_layer = target_ds.CreateLayer(output_layer_name, srs1, geom_type=ogr.wkbPolygon, options=["ENCODING=UTF-8"])
    ds = src_layer1.Erase(src_layer2, target_layer)
    ds = None