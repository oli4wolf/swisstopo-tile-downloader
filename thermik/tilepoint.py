from pygeotile.point import Point
from pygeotile.tile import Tile

"""_summary_
        Simplified Object for the basic handling. Reuniting pygeotile Tile and Point.
        Which don't change while working and are initialised through lat/lon and zoom.
    Returns:
        _type_: _description_
"""
class TilePoint:

    def __init__(self, latitude:float, longitude:float,zoom:float, tilesize:int):
        self.point = Point.from_latitude_longitude(latitude,longitude)
        self.tile = Tile.for_latitude_longitude(latitude,longitude,zoom)
        self.TILESIZE = tilesize
        self.ZOOM = zoom
            
    def getPixel(self):
        return self.point.pixels
        
    def getTile(self):
        return self.tile.google
        
    def getLatLon(self):
        return self.point.latitude_longitude
    
    def getLongitude(self):
        return self.point.latitude_longitude[1]
    
    def getLatitude(self):
        return self.point.latitude_longitude[0]
        
    def getTilePixel(self):
        return (self.point.pixels(self.ZOOM)[0] - (self.tile.google[0] * self.TILESIZE)), (self.point.pixels(self.ZOOM)[1] - (self.tile.google[1] * self.TILESIZE))
        
