import math
import os
import cv2
import requests
import numpy as np
from enum import Enum


class ImgSource(Enum):
    """
    #Google地图瓦片
    # tilepath = 'http://www.google.cn/maps/vt/pb=!1m4!1m3!1i'+str(zoom)+'!2i'+str(x)+'!3i'+str(y)+'!2m3!1e0!2sm!3i345013117!3m8!2szh-CN!3scn!5e1105!12m4!1e68!2m2!1sset!2sRoadmap!4e0'
    #Google影像瓦片
    # tilepath = 'http://mt3.google.cn/vt/lyrs=s@110&hl=zh-CN&gl=cn&src=app&x='+str(x)+'&y='+str(y)+'&z='+str(zoom)+'&s=G'
    #天地图-地图
    #tilepath = 'http://t4.tianditu.com/DataServer?T=vec_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=45c78b2bc2ecfa2b35a3e4e454ada5ce'
    #天地图-标注
    #tilepath = 'http://t3.tianditu.com/DataServer?T=cva_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=45c78b2bc2ecfa2b35a3e4e454ada5ce'
    #天地图-影像
    # tilepath = 'http://t2.tianditu.gov.cn/DataServer?T=img_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=2ce94f67e58faa24beb7cb8a09780552'
    #天地图-影像标注
    # tilepath = 'http://t2.tianditu.gov.cn/DataServer?T=cia_w&x='+str(x)+'&y='+str(y)+'&l='+str(zoom)+'&tk=2ce94f67e58faa24beb7cb8a09780552'
    #高德地图影像瓦片
    tilepath = "http://wprd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scl=1&style=6&x=" + str(x) + "&y=" + str(y) + "&z=" + str(zoom) + "&ltype=3"
    """
    GoogleMap = 0
    Tianditu = 1
    Gaode = 2
    #BLUE = 3

class LonLat:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

class XY:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y



class LoadOpenImg():
    """
    Download google-map satellite image
    #load_google_map_satellite

    Args:
        save_path : download image save path
        point_lonlat_lt : image left-top point (longitude,latitude)
        point_lonlat_rb : image right-bottom point (longitude,latitude)
        image_level: google earth map's image level
        img_source: ImgSource:[GoogleMap,Tianditu,Gaode] default=Gaode
        use_proxies: default=False, if True,connect with proxies
        proxies: connection's proxies address
    """
    def __init__(
            self,
            save_path,
            point_lonlat_lt: LonLat,
            point_lonlat_rb: LonLat,
            image_level,
            img_source: ImgSource = ImgSource.Gaode,
            use_proxies: bool=False,
            proxies = {
            "http": "socks5://127.0.0.1:10792",
            "https": "socks5h://127.0.0.1:10792"
            }
        ):
        self.save_path=save_path
        self.point_lonlat_lt = point_lonlat_lt
        self.point_lonlat_rb = point_lonlat_rb
        self.image_level = image_level
        self.image_source=img_source
        self.use_proxies=use_proxies
        self.proxies=proxies

        self.xy_lt=self.lonlatz2xy(self.point_lonlat_lt,self.image_level)
        self.xy_rb=self.lonlatz2xy(self.point_lonlat_rb,self.image_level)
    
    def build_url(self,xy):
        if self.image_source==ImgSource.GoogleMap:
             # TODO: support multi service choice
             return "http://khms0.google.com/kh/v=893?&x={x}&y={y}&z={z}".format(x=xy.x, y=xy.y, z=self.image_level)
        elif self.image_source==ImgSource.GoogleMap:
             # TODO: support multi service choice
             return "http://mt3.google.cn/vt/lyrs=s@110&hl=zh-CN&gl=cn&src=app&x={x}&y={y}&z={z}".format(x=xy.x, y=xy.y, z=self.image_level)
        elif self.image_source==ImgSource.Gaode:
             # TODO: support multi service choice
             return "http://wprd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scl=1&style=6&x={x}&y={y}&z={z}&ltype=3".format(x=xy.x, y=xy.y, z=self.image_level)
        else:
            print('The '+self.image_source+' is not support!')
            return ''

    def lonlatz2xy(self, lonlat, zoom):
        n = math.pow(2, zoom)
        x = ((lonlat.lon + 180) / 360) * n
        y = (1 - (math.log(math.tan(math.radians(lonlat.lat)) + (1 / math.cos(math.radians(lonlat.lat)))) / math.pi)) / 2 * n
        return XY(int(x),int(y))
    
    def xyz2lonlat(self,XY, z):
        n = math.pow(2, z)
        lon = XY.x / n * 360.0 - 180.0
        lat = math.atan(math.sinh(math.pi * (1 - 2 * XY.y / n)))
        lat = lat * 180.0 / math.pi
        return LonLat(lon,lat)
    
    def download(self, path, xy):
        """
        create url and download image
        """
        path = path + "\\{z}\\{x}\\".format(z=self.image_level, x=xy.x)
        url = self.build_url(xy)
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = path + "\\{y}.png".format(y=xy.y)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 400:
            print("skip")
            pass
        else:
            for x in range(0,3):
                session = requests.Session()
                if self.use_proxies:
                    response =session.get(url,proxies=self.proxies)
                else:
                    response =session.get(url)
                if response.status_code == 200:
                    #print('GET')
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    break;
                else:
                    print("network error!")
    def load(self):
        """
        main function
        """
        print(self.xy_lt.x, self.xy_lt.y, self.image_level)
        print(self.xy_rb.x, self.xy_rb.y, self.image_level)
        count = 0
        all = (self.xy_rb.x-self.xy_lt.x+1) * (self.xy_rb.y-self.xy_lt.y+1)
        for i in range(self.xy_lt.x, self.xy_rb.x+1):
            for j in range(self.xy_lt.y, self.xy_rb.y+1):
                self.download(self.save_path, XY(i, j))
                count += 1
                print("{m}/{n}".format(m=count, n=all))
                pass
        #self.merge()
    
    def merge(self,
              merge_image_name: str='merge',
              merge_image_format: str='png'
            ):
        """
        merge image
        """
        row_list = list()
        for i in range(self.xy_lt.x, self.xy_rb.x+1):
            col_list = list()
            for j in range(self.xy_lt.y, self.xy_rb.y+1):
                col_list.append(cv2.imread(self.save_path + "\\{z}\\{i}\\{j}.png".format(i=i, j=j,z=self.image_level)))
            k = np.vstack(col_list)
            row_list.append(k)
        result = np.hstack(row_list)
        cv2.imwrite(self.save_path +'/'+merge_image_name+'_'+str(self.image_level)+'.'+merge_image_format, result)

    