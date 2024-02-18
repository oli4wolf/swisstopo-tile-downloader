"""
The idea is to input KML and all the points will be added to the respective point.dat file.
/zoomlevel/x-tile/y-tile_point.dat
"""

class GeneratePointsDat():
    def __init__(self, zoom=None):
        # Default values
        if zoom is None:
            zoom = 15  # maximum zoom level for DEM5A data
        self.zoom = int(zoom)

    @classmethod
    def generatePointsDat(self, zoom, coordinate):
        #calculate point coordinates
        
        #if file exist append else create file.
        
        return ''

    @classmethod
    def generatePointsDat(self, zoom, lon, lat):
        return ''