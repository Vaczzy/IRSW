import os
from Cliper import Cliper
"""
运行main.py执行裁剪:
    -txtPath: 影像和矢量的对应关系txt
      见example.txt:
      格式：
        tif影像完整路径\t对应shp标签名称
    -tempRasterPath: 无需设定
    -resultFile: 裁剪后影像的保存文件夹
"""


if __name__=='__main__':
    txtPath=r"/home/csu/Downloads/cq_segment/cq_mmseg/cliper/example.txt" # 影像和矢量的对应关系txt 
    tempRasterPath=r"/home/csu/Downloads/cq_segment/cq_mmseg/cliper/tempdata/temp.tif" # 中间文件
    resultFile=r"/home/csu/Downloads/cq_segment/cq_mmseg/cliper/result" # 裁剪后影像的保存路径

    cliper=Cliper(resultFile,tempRasterPath,size=512,step=512)

    lines=None
    with open(txtPath, 'r') as f:
        lines= f.readlines()
    for line in lines:
        tifPath,shpname = line.strip().split('\t')
        shpPath = os.path.join(r"/home/csu/Downloads/cq_segment/cq_mmseg/cliper/data/", shpname) # 影像对应的标签路径在此修改
        print("正在处理:{}".format(os.path.basename(shpname)))
        cliper.SampleSingleTif(tifPath, shpPath)

        os.remove(tempRasterPath)

