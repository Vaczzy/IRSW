from osgeo import gdal
import numpy as np
import os
from tqdm import tqdm
import utils

class Cliper(object):
    def __init__(self, resultFile, tempRasterPath, size=512,step=256,clipratio=0.2):
        self.size=size # image size
        self.step=step # step
        self.resultFile= resultFile
        self.tempRasterPath = tempRasterPath
        self.index=0
        self.clipratio = clipratio
        self.tifResolution = None
        self.sampleNegData = True
        self.pngDriver = gdal.GetDriverByName("PNG")
        self.memDriver =gdal.GetDriverByName("MEM")

    def SetTifresolution(self, resolution):
        self.tifResolution = resolution

    def SampleSingleTif(self,tifPath,shpPath):
        tifDS =utils.ReadGdalDataset(tifPath)
        self.SetTifresolution(abs(tifDS.GetGeoTransform()[1]))
        shpDS = utils.ReadShpDataset(shpPath)
        
        layer = shpDS.GetLayer(0)

        utils.Shp2Raster(self.tempRasterPath, layer, tifDS.RasterXSize, tifDS.RasterYSize,
                        tifDS.GetGeoTransform(), tifDS.GetProjection())
        maskDS = utils.ReadGdalDataset(self. tempRasterPath)
        self.Sample(tifDS,maskDS)
        
        del tifDS
        del shpDS
        del maskDS

    def Sample(self, tifDS, maskDS):
        # dstFile = os.path.join(self.resultFile, str(self.tifResolution))
        # self.DirectoryCheck(dstFile)
        
        imgDstFile= os.path.join(self.resultFile, "images")
        lblDstFile = os.path.join(self.resultFile, "labels")
        if not os.path.exists(imgDstFile):
            os.makedirs(imgDstFile)
        if not os.path.exists(lblDstFile):
            os.makedirs(lblDstFile)
        
        for j in tqdm(range(0, tifDS.RasterYSize - self.size, self.step)):
            for i in range(0, tifDS.RasterXSize - self.size, self.step):
                tifBlock = tifDS.ReadAsArray(i,j,self.size, self.size)
                tifBlock = tifBlock[0:3,:,:]

                labelBlock = maskDS.ReadAsArray(i,j,self.size, self.size)
                labelBlock = np.expand_dims (labelBlock,0)
                labelBlock = labelBlock / 255.0
                labelBlock = labelBlock.astype(np.int8)
                
                labeltype = "pos"
                s= np.sum(labelBlock > 0)
                if s<0:
                    continue
                elif s ==0:
                    if np.sum(tifBlock) ==0:
                        continue
                #elif random.randint(0, 200)>1:# continue
                    else:
                        labeltype="neg"
                
                index = len(os.listdir(imgDstFile))
                imgPath = os.path.join(imgDstFile,"{}_{}.png".format(str(index), labeltype))
                labelPath = os.path.join(lblDstFile, "{}_{}.png".format(str(index),labeltype))

                self.SaveBlock(tifBlock,imgPath, self.size,self.size, 3,self.GetTifDatatype(tifBlock))
                self.SaveBlock(labelBlock, labelPath, self.size, self.size, 1,self.GetTifDatatype(labelBlock))
    
    def SaveBlock(self, ds, path, w,h,channels, dtype):
        createdDS = self.memDriver.Create("",w, h,channels, dtype)
        for band in range(channels):
            createdDS.GetRasterBand(band + 1).WriteArray(ds[band])
        self.pngDriver.CreateCopy(path,createdDS)

    def GetTifDatatype(self,imBlock):
        dataType=None
        if 'int8' in imBlock.dtype.name:
            dataType = gdal.GDT_Byte
        elif 'int16' in imBlock.dtype.name:
            dataType = gdal.GDT_UInt16
        else:
            dataType = gdal.GDT_Float32
        
        if dataType==None:
            print("Data type of sat image is not support!")
            exit(0)
        return dataType

    