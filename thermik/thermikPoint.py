# URL KK7 https://thermal.kk7.ch/api/hotspots/csv/all_all/46.1,7.311,46.698,8.689
# WGS84: 5.8358140744676303 45.659168946713827 10.979311848153316 47.869910020393519
import csv
import requests
import shutil
from tilepoint import TilePoint
import os

path = "./thermik/"


def deleteOldHotspots(zoom):
    if os.path.exists(path+str(zoom)):
        shutil.rmtree(path+str(zoom))


def downloadKK7Hotspots():
    url = "https://thermal.kk7.ch/api/hotspots/csv/all_all/45.659168946713827,5.8358140744676303,47.869910020393519,11.0"
    r = requests.get(url)
    if (r.status_code != 200):
        exit
    with open(path+"hotspots.csv", 'wb') as f:
        f.write(r.content)
    return path+"hotspots.csv"


def writeAppendPoint(zoom, name, tile_x, tile_y, pxl_x, pxl_y, geometryType, i):
    if not os.path.exists(path+str(zoom)+"/"+str(tile_x)+"/"):
        os.makedirs(path+str(zoom)+"/"+str(tile_x)+"/")
    with open(path+str(zoom)+"/"+str(tile_x)+"/"+str(tile_y)+"_hotspot.dat", 'a+') as f:
        f.write(""+name+","+str(i)+","+geometryType+","+str(pxl_x)+","+str(pxl_y)+"\n")


def readKK7Hotspots(zoom):
    with open(path+"hotspots.csv", "r") as f:
        reader = csv.reader(f, delimiter="\t")
        next(reader)  # Skip the first line
        for i, line in enumerate(reader):
            #46.63365,7.64855,1750,96
            lat, lon, height, percentage = line[0].split(',')[:4]
            tilePoint = TilePoint(float(lat), float(lon), zoom, 256)
            writeAppendPoint(zoom, str(height), tilePoint.getTile()[0], tilePoint.getTile()[1], tilePoint.getTilePixel()[0], tilePoint.getTilePixel()[0], "Thermal", percentage)


def main():
    #downloadKK7Hotspots()
    for zoom in range(12, 16):
        deleteOldHotspots(zoom)
        readKK7Hotspots(zoom)

if __name__ == "__main__":
    main()