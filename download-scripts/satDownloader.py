'''
https://wmts.geo.admin.ch/EPSG/3857/1.0.0/WMTSCapabilities.xml

<ResourceURL format="image/jpeg" resourceType="tile" template="https://wmts.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/{Time}/4326/{TileMatrix}/{TileCol}/{TileRow}.jpeg"/>

z,x,y
Lehn: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/15/17094/11567.jpeg
Chancy: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/15/16927/11640.jpeg
Martina: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/15/17337/11540.jpeg
Basel: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/15/17162/11415.jpeg
chiasso: https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/15/17206/11682.jpeg
x 
Weissenbühl etwa
https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/15/17059/11533.jpeg


<ows:Identifier>3857_19</ows:Identifier>

.open "C:/Users/u214033/OneDrive - SBB/Projekte/m5stack-collision-warning/tiles.db"
'''

import os
import re
from tileCalculation import GlobalMercator

import asyncio
import aiohttp
import aiofiles
import datetime

path = "./map/"
urls=[]

async def fileDownload(url: str, zoom: int, x: int, y: int):
    retry = True
    while retry:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if not os.path.exists(path+str(zoom)+"/"+str(x)):
                        os.makedirs(path+str(zoom)+"/"+str(x))
                    async with aiofiles.open(path+str(zoom)+"/"+str(x)+"/"+str(y)+".jpeg", "wb") as f:
                        content = await response.read()
                        if len(content) > 810:
                            await f.write(content)
                        retry = False
        except aiohttp.ClientError:
                # sleep a little and try again
                await asyncio.sleep(1)
        except Exception as e:
                # sleep a little and try again
                print(e)
                await asyncio.sleep(1)

def initializeAndLaunch(z:int):
    #Bounding box
    #<ows:LowerCorner>5.140242 45.398181</ows:LowerCorner>
    #<ows:UpperCorner>11.47757 48.230651</ows:UpperCorner>
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
            urls.append("https://wmts3.geo.admin.ch/1.0.0/ch.swisstopo.swissimage/default/current/3857/"+str(z)+"/"+str(x)+"/"+str(y)+".jpeg")
    return urls

async def main(filepath, download):
    now = datetime.datetime.now()
    print(now.time())
    path = filepath+"map/"
    if not os.path.exists(path):
        os.makedirs(path)
    if download:
        for z in range(13,16,1):
            urls = initializeAndLaunch(z)
    # Split the urls list into chunks of 1000 elements each
            chunks = [urls[i:i+1000] for i in range(0, len(urls), 1000)]
            # Process each chunk asynchronously
            for chunk in chunks:
                async with asyncio.TaskGroup() as group:
                    for url in chunk:
                        zoom = re.search(r'/3857/(\d+)', url).group(1)
                        zoom_pattern = rf'/{zoom}/(\d+)'
                        tile_x = re.search(zoom_pattern, url).group(1)
                        tile_x_pattern = rf'/{tile_x}/(\d+)'
                        tile_y = re.search(tile_x_pattern, url).group(1)
                        group.create_task(fileDownload(url, zoom, tile_x, tile_y))
        now = datetime.datetime.now()
        print(now.time())

# python thermikPoint.py debug 46.63365,7.64855,1750,96
if __name__ == "__main__":
    asyncio.run(main("./", True))