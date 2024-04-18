'''
https://wmts.geo.admin.ch/EPSG/3857/1.0.0/WMTSCapabilities.xml

<ResourceURL format="image/jpeg" resourceType="tile" template="https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/{Time}/4326/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>

z,x,y
Lehn: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/17094/11567.jpeg
Chancy: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/16927/11640.jpeg
Martina: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/17337/11540.jpeg
Basel: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/17162/11415.jpeg
chiasso: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/17206/11682.jpeg
x 
Weissenbühl etwa
https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/17059/11533.jpeg


<ows:Identifier>3857_19</ows:Identifier>

.open "C:/Users/u214033/OneDrive - SBB/Projekte/m5stack-collision-warning/tiles.db"
'''

import os
import re
#from aiohttp import request
from concurrent.futures import ThreadPoolExecutor
import requests
from tileCalculation import GlobalMercator

path = "./map/"

cnt = 0
def saveFile(zoom, x, y, tile):
        if not os.path.exists(path+str(zoom)+"/"+str(x)):
            os.makedirs(path+str(zoom)+"/"+str(x))
        with open(path+str(zoom)+"/"+str(x)+"/"+str(y)+".jpeg", 'wb') as f:
            f.write(tile)
            f.close

def download(url):
    response = requests.get(url)
    if response.status_code == 200:
        temp = re.findall(r'\d+', url)
        val = list(map(int, temp))
        img_data = response.content
        if val[6]%100==0:
            print(len(img_data),url)
        if(len(img_data)>810):
            saveFile(val[5],val[6],val[7],img_data)

def initializeAndLaunch():
    urls=[]
    #Bounding box
    #<ows:LowerCorner>5.140242 45.398181</ows:LowerCorner>
    #<ows:UpperCorner>11.47757 48.230651</ows:UpperCorner>
    for z in range(12,16,1):
        #LowerCorner
        gm = GlobalMercator()
        mx = gm.LatLonToMeters(45.398181,5.140242)[0]
        my = gm.LatLonToMeters(45.398181,5.140242)[1]
        px = gm.MetersToPixels(mx,my,z)[0]
        py = gm.MetersToPixels(mx,my,z)[1]
        lowerTileX = gm.PixelsToTile(px,py)[0]
        upperTileY = gm.PixelsToTile(px,py)[1]
        print(gm.PixelsToTile(px,py))
        #UpperCorner
        mx = gm.LatLonToMeters(48.230651, 11.47757)[0]
        my = gm.LatLonToMeters(48.230651, 11.47757)[1]
        px = gm.MetersToPixels(mx,my,z)[0]
        py = gm.MetersToPixels(mx,my,z)[1]
        upperTileX = gm.PixelsToTile(px,py)[0]
        lowerTileY = gm.PixelsToTile(px,py)[1]
        print(gm.PixelsToTile(px,py))
        for y in range(lowerTileY,upperTileY+1,1):
            for x in range(lowerTileX, upperTileX+1,1):
                urls.append("https://wmts3.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/"+str(z)+"/"+str(x)+"/"+str(y)+".jpeg")

    with ThreadPoolExecutor(max_workers=32) as executor:
        executor.map(download, urls) #urls=[list of url] 

def main(path, download):
    path = path+"map/"
    if not os.path.exists(path):
        os.makedirs(path)
    if download:
        initializeAndLaunch()

# python thermikPoint.py debug 46.63365,7.64855,1750,96
if __name__ == "__main__":
    main("./", True)