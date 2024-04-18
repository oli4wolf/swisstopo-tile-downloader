import glob
import os
import shutil
import sys
from xml.dom import minidom
import requests, zipfile, io

from calc_segment import Segment
from tilepoint import TilePoint

import os

path = "./obstacles/"
url = "https://data.geo.admin.ch/ch.bazl.luftfahrthindernis/luftfahrthindernis/luftfahrthindernis_4326.kmz"
verbose = False
TILESIZE = 256 #Fixed Size from the wmts service manually entered.
INSIDE, LEFT, RIGHT, TOP, BELOW = 0, 1, 2, 4, 8
COUNTER = 0

"""
Structure Download actual file.
Delete existing KML
Decompress KMZ -> KML.
Reinitialize Obstacle.
Read KML and
Generate Points.
Generate lines.
"""
def deleteKMZandKML():
    # get a recursive list of file paths that matches pattern including sub directories
    fileList = glob.glob(path+"*.kml")
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")    
    # get a recursive list of file paths that matches pattern including sub directories
    fileList = glob.glob(path+"*.sha512")
    # Iterate over the list of filepaths & remove each file.
    for filePath in fileList:
        try:
            os.remove(filePath)
        except OSError:
            print("Error while deleting file")    

def downloadKMZtoKML(url):
    r = requests.get(url)
    if(r.status_code != 200):
        exit
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(path)
    
def deleteOldObstacles(zoom):
    if os.path.exists(path+str(zoom)):
        shutil.rmtree(path+str(zoom))
        
def readKMLObstacles(zoom):
    #parse xml file
    fileList = glob.glob(path+"*.kml")
    print(fileList)
    readKML(fileList[0],zoom)

def readKML(filepath, zoom):
    file = minidom.parse(filepath)
    #grab all <record> tags
    placemarks = file.getElementsByTagName("Placemark")
    
    for placemark in placemarks:
        if placemark.getElementsByTagName("LineString"):
            # Idea with line is pretty simple go from the first to the second until the last coordinate.
            # If the Coordinate does cross multiple coordinates recalculate with the next to the second.
            name = placemark.getElementsByTagName("name")[0].firstChild.nodeValue
            if verbose:
                print("LineString: ")
                print(placemark.getElementsByTagName("coordinates")[1].firstChild.nodeValue)
            coords = placemark.getElementsByTagName("coordinates")[1].firstChild.nodeValue.split(' ')
            global COUNTER
            COUNTER = 0
            recursiveLineToTile(zoom, coords,name)

        # Point
        elif placemark.getElementsByTagName("Point"):
            coords = placemark.getElementsByTagName("coordinates")[0].firstChild.nodeValue.split(',')
            name = placemark.getElementsByTagName("name")[0].firstChild.nodeValue
            tilePoint = TilePoint(float(coords[1]),float(coords[0]),zoom,TILESIZE)
            writeAppendPoint(zoom,name,tilePoint.getTile()[0],tilePoint.getTile()[1],
                                tilePoint.getTilePixel()[0],tilePoint.getTilePixel()[0],
                                "Point",0) #Todo improve with obstacleType
    return

def recursiveLineToTile(zoom, coords, name):
    fromTilePoint = None
    for geoCoordinate in coords:
        if fromTilePoint == None:
            fromTilePoint = TilePoint(float(geoCoordinate.split(',')[1]),float(geoCoordinate.split(',')[0]),zoom,TILESIZE)
        else:
            toTilePoint=TilePoint(float(geoCoordinate.split(',')[1]),float(geoCoordinate.split(',')[0]),zoom,TILESIZE)
            
            lineToTile(zoom, fromTilePoint, toTilePoint, name)
            
            # After calculation
            fromTilePoint = toTilePoint
            #print("check this")

def lineToTile(zoom:int, fromTilePoint:TilePoint, toTilePoint:TilePoint, name:str):
    #Calculate Segments
            result = Segment.determineCaseAndIntersection(zoom,fromTilePoint.getLongitude(),fromTilePoint.getLatitude(),
                                  toTilePoint.getLongitude(), toTilePoint.getLatitude())
            #INSIDE, LEFT, RIGHT, TOP, BELOW = 0, 1, 2, 4, 8
            if result[0] == INSIDE:
                #Inside means both points are in the same Tile so in the same file 
                # and no further calculation needed.
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                fromTilePoint.getTilePixel()[0],fromTilePoint.getTilePixel()[1],
                                "LineString")
                writeAppendLine(zoom,name,toTilePoint.getTile()[0],toTilePoint.getTile()[1],
                                toTilePoint.getTilePixel()[0],toTilePoint.getTilePixel()[1],
                                "LineString")
                return
            elif result[0] == LEFT:
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                fromTilePoint.getTilePixel()[0],fromTilePoint.getTilePixel()[1],
                                "LineString")
                # Tile stays the same but the new coordinates is used for another calculation
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                result[2][0],result[2][1],
                                "LineString")
                lineToTile(zoom,TilePoint(result[1][0],result[1][1],zoom,TILESIZE),toTilePoint,name)
            elif result[0] == RIGHT:
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                fromTilePoint.getTilePixel()[0],fromTilePoint.getTilePixel()[1],
                                "LineString")
                # Tile stays the same but the new coordinates is used for another calculation
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                result[2][0],result[2][1],
                                "LineString")
                lineToTile(zoom,TilePoint(result[1][0],result[1][1],zoom,TILESIZE),toTilePoint,name)
            elif result[0] == TOP:
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                fromTilePoint.getTilePixel()[0],fromTilePoint.getTilePixel()[1],
                                "LineString")
                # Tile stays the same but the new coordinates is used for another calculation
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                result[2][0],result[2][1],
                                "LineString")
                lineToTile(zoom,TilePoint(result[1][0],result[1][1],zoom,TILESIZE),toTilePoint,name)
            elif result[0] == BELOW:
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                fromTilePoint.getTilePixel()[0],fromTilePoint.getTilePixel()[1],
                                "LineString")
                # Tile stays the same but the new coordinates is used for another calculation
                writeAppendLine(zoom,name,fromTilePoint.getTile()[0],fromTilePoint.getTile()[1],
                                result[2][0],result[2][1],
                                "LineString")
                lineToTile(zoom,TilePoint(result[1][0],result[1][1],zoom,TILESIZE),toTilePoint,name)
            else:
                print("Unexpected Case")
            return

def writeAppendLine(zoom, name, tile_x, tile_y, idx_x, idx_y, geometryType):
    global COUNTER
    if not os.path.exists(path+str(zoom)+"/"+str(tile_x)+"/"):
        os.makedirs(path+str(zoom)+"/"+str(tile_x)+"/")
    with open(path+str(zoom)+"/"+str(tile_x)+"/"+str(tile_y)+"_line.dat", 'a+') as f:
        f.write(""+name+","+str(COUNTER)+","+geometryType+","+str(idx_x)+","+str(idx_y)+"\n")
    COUNTER = COUNTER+1
    return

def writeAppendPoint(zoom, name, tile_x, tile_y, idx_x, idx_y, geometryType, i):
    if not os.path.exists(path+str(zoom)+"/"+str(tile_x)+"/"):
        os.makedirs(path+str(zoom)+"/"+str(tile_x)+"/")
    with open(path+str(zoom)+"/"+str(tile_x)+"/"+str(tile_y)+"_point.dat", 'a+') as f:
        f.write(""+name+","+str(i)+","+geometryType+","+str(idx_x)+","+str(idx_y)+"\n")


def main(path, download):
    path = path+"obstacles/"
    if not os.path.exists(path):
        os.makedirs(path)
    if download:
        deleteKMZandKML()
        downloadKMZtoKML(url)
    for zoom in range(12, 16):
        deleteOldObstacles(zoom)
        readKMLObstacles(zoom)

def debug(line):
    lat, lon, height, percentage = line.split(',')[:4]
    print(lat, lon, height, percentage)
    tilePoint = TilePoint(float(lat), float(lon), 15, 256)
    print(tilePoint.getTile())
    print(tilePoint.getTilePixel())

# python thermikPoint.py debug 46.63365,7.64855,1750,96
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        debug(sys.argv[2])
    else:
        main("./", True)
