import math
from tkinter.tix import MAX
class GlobalMercator(object):
    def __init__(self, tileSize=256):
    #        "Initialize the TMS Global Mercator pyramid"
        self.tileSize = tileSize
        self.initialResolution = 2 * math.pi * 6378137 / self.tileSize
        # 156543.03392804062 for tileSize 256 pixels
        self.originShift = 2 * math.pi * 6378137 / 2.0
        # 20037508.342789244

    def LatLonToMeters(self, lat, lon ):
    #       "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
        mx = lon * self.originShift / 180.0
        my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)
        my = my * -self.originShift / 180.0
        return mx, my

    def MetersToPixels(self, mx, my, zoom):
            #"Converts EPSG:900913 to pyramid pixel coordinates in given zoom level"               
        res = self.Resolution( zoom )
        px = (mx + self.originShift) / res
        py = (my + self.originShift) / res
        return px, py
        
    def PixelsToTile(self, px, py):
        #"Returns a tile covering region in given pixel coordinates"
        tx = int( math.ceil( px / float(self.tileSize) ) - 1 )
        ty = int( math.ceil( py / float(self.tileSize) ) - 1 )
        return tx, ty
    
    def Resolution(self, zoom ):
        "Resolution (meters/pixel) for given zoom level (measured at Equator)"
        # return (2 * math.pi * 6378137) / (self.tileSize * 2**zoom)
        return self.initialResolution / (2**zoom)


def debug():
    '''
    Weissenbühl etwa
    https://wmts10.geo.admin.ch/1.0.0/ch.swisstopo.pixelkarte-farbe/default/current/3857/15/17059/11533.jpeg
    46.935598, 7.431087
    '''

    gm = GlobalMercator()
    zoom = 15
    lat = 46.935598
    lon = 7.431087
    mx = gm.LatLonToMeters(lat, lon)[0]
    my = gm.LatLonToMeters(lat, lon)[1]
    print(gm.LatLonToMeters(lat, lon))
    px = gm.MetersToPixels(mx,my,zoom)[0]
    py = gm.MetersToPixels(mx,my,zoom)[1]
    print(gm.MetersToPixels(mx,my,zoom))
    tx = gm.PixelsToTile(px,py)[0]
    ty = gm.PixelsToTile(px,py)[1]
    print(gm.PixelsToTile(px,py))

    '''
    BoundingBox EPSG 3857
    '''
    zoom = 15
    lat = 45.398181
    lon = 5.140242 
    mx = gm.LatLonToMeters(lat, lon)[0]
    my = gm.LatLonToMeters(lat, lon)[1]
    print(gm.LatLonToMeters(lat, lon))
    px = gm.MetersToPixels(mx,my,zoom)[0]
    py = gm.MetersToPixels(mx,my,zoom)[1]
    print(gm.MetersToPixels(mx,my,zoom))
    tx = gm.PixelsToTile(px,py)[0]
    ty = gm.PixelsToTile(px,py)[1]
    print(gm.PixelsToTile(px,py))

    zoom = 15
    lat = 48.230651
    lon = 11.47757
    mx = gm.LatLonToMeters(lat, lon)[0]
    my = gm.LatLonToMeters(lat, lon)[1]
    print(gm.LatLonToMeters(lat, lon))
    px = gm.MetersToPixels(mx,my,zoom)[0]
    py = gm.MetersToPixels(mx,my,zoom)[1]
    print(gm.MetersToPixels(mx,my,zoom))
    tx = gm.PixelsToTile(px,py)[0]
    ty = gm.PixelsToTile(px,py)[1]
    print(gm.PixelsToTile(px,py))

    print("Nidau")
    zoom = 15
    lat = 47.12750
    lon = 7.23314
    mx = gm.LatLonToMeters(lat, lon)[0]
    my = gm.LatLonToMeters(lat, lon)[1]
    print(gm.LatLonToMeters(lat, lon))
    px = gm.MetersToPixels(mx,my,zoom)[0]
    py = gm.MetersToPixels(mx,my,zoom)[1]
    print(gm.MetersToPixels(mx,my,zoom))
    tx = gm.PixelsToTile(px,py)[0]
    ty = gm.PixelsToTile(px,py)[1]
    print(gm.PixelsToTile(px,py))