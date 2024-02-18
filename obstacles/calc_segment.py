from pygeotile.point import Point
from pygeotile.tile import Tile

import pylineclip

TILE_SIZE = 256
INSIDE, LEFT, RIGHT, TOP, BELOW = 0, 1, 2, 4, 8

class Segment:
    def determinPixelFromTile(zoom:int, p:Point, t:Tile):
        return (p.pixels(zoom)[0] - (t.google[0] * TILE_SIZE)), (p.pixels(zoom)[1] - (t.google[1] * TILE_SIZE))

        """Determine Case
        check if the line passes the limits of the tile and call the next loop for the next Step.
        """
    def determineCaseAndIntersection(zoom, lon1, lat1, lon2,lat2):
        p1 = Point.from_latitude_longitude(lat1,lon1)
        t1 = Tile.for_latitude_longitude(lat1,lon1, zoom)
        
        p2 = Point.from_latitude_longitude(lat2,lon2)
        t2 = Tile.for_latitude_longitude(lat2,lon2, zoom)
        
        if (t1.tms_x == t2.tms_x and t1.tms_y == t2.tms_y):
            return 0,0,0,0,0
        if (t1.tms_x != t2.tms_x or t1.tms_x != t2.tms_y):
                #Calculate Bounds of tile
                pBTopLeft=Point.from_latitude_longitude(t1.bounds[0].latitude, t1.bounds[0].longitude)
                pBBottomRight=Point.from_latitude_longitude(t1.bounds[1].latitude, t1.bounds[1].longitude)
                #xmin: float, ymax: float, xmax: float, ymin: float, x1: float, y1: float, x2: float, y2: float
                pcRes = pylineclip.cohensutherland(pBTopLeft.pixels(zoom)[0], pBTopLeft.pixels(zoom)[1], pBBottomRight.pixels(zoom)[0], pBBottomRight.pixels(zoom)[1], p1.pixels(zoom)[0], p1.pixels(zoom)[1],
                                    p2.pixels(zoom)[0], p2.pixels(zoom)[1])
                intersectionPoint = Point.from_pixel(pcRes[2],pcRes[3],zoom)
                print(Segment.determinPixelFromTile(zoom,intersectionPoint,t1))
                
                # if x = 0 then left so one tile less but what is the value?
                # Left
                if Segment.determinPixelFromTile(zoom,intersectionPoint,t1)[0]==0:
                    print("Left")
                    next = Point.from_pixel(intersectionPoint.pixels(zoom)[0]-1,intersectionPoint.pixels(zoom)[1],zoom)
                    intersection = Segment.determinPixelFromTile(zoom,intersectionPoint,t1)
                    return LEFT, next.latitude_longitude, intersection
                elif Segment.determinPixelFromTile(zoom,intersectionPoint,t1)[0]>=256:
                    print("Right")
                    next = Point.from_pixel(intersectionPoint.pixels(zoom)[0]+1,intersectionPoint.pixels(zoom)[1],zoom)
                    intersection = Segment.determinPixelFromTile(zoom,intersectionPoint,t1)
                    return RIGHT, next.latitude_longitude, intersection
                elif Segment.determinPixelFromTile(zoom,intersectionPoint,t1)[1]==0:
                    print("Top")
                    next = Point.from_pixel(intersectionPoint.pixels(zoom)[0],intersectionPoint.pixels(zoom)[1]-1,zoom)
                    intersection = Segment.determinPixelFromTile(zoom,intersectionPoint,t1)
                    return TOP, next.latitude_longitude, intersection
                elif Segment.determinPixelFromTile(zoom,intersectionPoint,t1)[1]>= 256:
                    print("Below")
                    next = Point.from_pixel(intersectionPoint.pixels(zoom)[0],intersectionPoint.pixels(zoom)[1]+1,zoom)
                    intersection = Segment.determinPixelFromTile(zoom,intersectionPoint,t1)
                    return BELOW, next.latitude_longitude, intersection
        return 
    
        """Return the intersection coordinate of this coordinates line.
        """
    def determineIntersection(zoom, lon1, lat1, lon2,lat2):
        p1 = Point.from_latitude_longitude(lat1,lon1)
        t1 = Tile.for_latitude_longitude(lat1,lon1, zoom)
        
        p2 = Point.from_latitude_longitude(lat2,lon2)
        t2 = Tile.for_latitude_longitude(lat2,lon2, zoom)
        
        result = []
        if (t1.tms_x == t2.tms_x and t1.tms_y == t2.tms_y):
            result.append(Segment.determinPixelFromTile(zoom,p1,t1))
            result.append(Segment.determinPixelFromTile(zoom,p2,t2))
        if (t1.tms_x != t2.tms_x or t1.tms_x != t2.tms_y):
                #Calculate Bounds of tile
                pBTopLeft=Point.from_latitude_longitude(t1.bounds[0].latitude, t1.bounds[0].longitude)
                pBBottomRight=Point.from_latitude_longitude(t1.bounds[1].latitude, t1.bounds[1].longitude)
                #xmin: float, ymax: float, xmax: float, ymin: float, x1: float, y1: float, x2: float, y2: float
                pcRes = pylineclip.cohensutherland(pBTopLeft.pixels(zoom)[0], pBTopLeft.pixels(zoom)[1], pBBottomRight.pixels(zoom)[0], pBBottomRight.pixels(zoom)[1], p1.pixels(zoom)[0], p1.pixels(zoom)[1],
                                    p2.pixels(zoom)[0], p2.pixels(zoom)[1])
                intersectionPoint = Point.from_pixel(pcRes[2],pcRes[3],zoom)
                result.append(Segment.determinPixelFromTile(zoom,intersectionPoint,t1))
                result.append(Segment.determinPixelFromTile(zoom,Point.from_pixel(pcRes[0],pcRes[1],zoom),t1))
        return result

#Segment.determineCaseAndIntersection(15, 8.931515333112547, 46.88518182848203, 8.903220300949611, 46.8879590176459)