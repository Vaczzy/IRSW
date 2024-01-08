import math
import os
import cv2
import requests
import numpy as np

class LonLat:
    def __init__(self, lon, lat):
        self.lon = lon
        self.lat = lat

class XY:
    def __init__(self, x: int, y:int):
        self.x = x
        self.y = y

class LoadGoogleImg():
    """
    Download google-map satellite image
    #load_google_map_satellite

    Args:
        save_path : download image save path
        point_lonlat_lt : image left-top point (longitude,latitude)
        point_lonlat_rb : image right-bottom point (longitude,latitude)
        image_level: google earth map's image level
    """
    def __init__(
            self,
            save_path,
            point_lonlat_lt: LonLat,
            point_lonlat_rb: LonLat,
            image_level,
            proxies = {
            "http": "socks5://127.0.0.1:8080",
            "https": "socks5h://127.0.0.1:8080"
        }
            ):
        self.save_path=save_path
        self.point_lonlat_lt = point_lonlat_lt
        self.point_lonlat_rb = point_lonlat_rb
        self.image_level = image_level
        self.proxies=proxies

        self.xy_lt=self.lonlatz2xy(self.point_lonlat_lt,self.image_level)
        self.xy_rb=self.lonlatz2xy(self.point_lonlat_rb,self.image_level)


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
    
    def build_url(self,xy):
        return "http://khms0.google.com/kh/v=893?&x={x}&y={y}&z={z}".format(x=xy.x, y=xy.y, z=self.image_level)

    
    def download(self, path, url, xy):
        path = path + "\\{z}\\{x}\\".format(z=self.image_level, x=xy.x)
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = path + "\\{y}.png".format(y=xy.y)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 400:
            print("skip")
            pass
        else:
            for x in range(0,3):
                session = requests.Session()
                response =session.get(url,proxies=self.proxies)
                #response = requests.get(url, proxies=self.proxies)
                if response.status_code == 200:
                    with open(filepath, "wb") as f:
                        f.write(response.content)
                    break;
                else:
                    print("network error!")
    
    def merge(self):
        row_list = list()
        for i in range(self.xy_lt.x, self.xy_rb.x+1):
            col_list = list()
            for j in range(self.xy_lt.y, self.xy_rb.y+1):
                col_list.append(cv2.imread(self.save_path + "\\{z}\\{i}\\{j}.png".format(i=i, j=j,z=self.image_level)))
            k = np.vstack(col_list)
            row_list.append(k)
        result = np.hstack(row_list)
        cv2.imwrite(self.save_path + "//merge.png", result)

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
                url = self.build_url(XY(i, j))
                self.download(self.save_path,url, XY(i, j))
                count += 1
                print("{m}/{n}".format(m=count, n=all))
                pass
        self.merge()