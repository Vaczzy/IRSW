from utils.load import LoadImg

if __name__ == '__main__':
    # 存储目录
    path = r"C:/IRSW/TEST"
     
    level_start = 16
    level_end = 17
    
    for i in range(level_start,level_end+1):
        loader=LoadImg.LoadGoogleImg(path,
                                     LoadImg.LonLat(116.286476, 40.069985),
                                     LoadImg.LonLat(116.324707 ,40.054938),
                                     i)
        loader.load()