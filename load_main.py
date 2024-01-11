from utils.load import LoadImg

if __name__ == '__main__':
    # 存储目录
    path = r"C:/IRSW/TEST2"
    
    level_start = 16
    level_end = 17
    
    # LeftTop=LoadImg.LonLat(116.286476, 40.069985),
    # RightBottom=LoadImg.LonLat(116.324707 ,40.054938),

    LeftTop=LoadImg.LonLat(116.38548052911783,39.921328173163715),
    RightBottom=LoadImg.LonLat(116.39726126581404,39.906787231227604),

    for i in range(level_start,level_end+1):
        loader=LoadImg.LoadOpenImg(path,
                                     LoadImg.LonLat(116.38548052911783,39.921328173163715),
                                     LoadImg.LonLat(116.39726126581404,39.906787231227604),
                                     i)
        loader.load()
        loader.merge()