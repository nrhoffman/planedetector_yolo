import cv2
import math
import numpy as np
import os
import requests

class TileCreator():
    """
    A class representing the tiles that make up a whole image

    Attributes:
        self.tiles = matrix of tiles
    """
    def __init__(self, lat1, lon1, lat2, lon2):
        """ Inits the class """
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.zoom = 16
        self.tiles = self.generateTiles()
    
    def generateTiles(self):
        """ Generates a matrix of tiles for processing"""
        api_key = os.getenv('API_KEY')
        x1, y1, x2, y2 = self.getTileLimits()
        print(f"Tile limits: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
        tiles = []
        num_tiles = (x2 - x1 + 1)*(y2 - y1 + 1)

        # Iterates through the y limits
        for y in range(y1, y2 + 1):
            tile = []

            # Iterates through the x limits
            for x in range(x1, x2 + 1):
                cur_tile = (y - y1) * (x2 - x1 + 1) + (x - x1 + 1)
                print(f"Retrieving Tile: {cur_tile} of {num_tiles}")
                center = self.tileToLatLon(x, y, self.zoom)
                url = f"https://maps.googleapis.com/maps/api/staticmap?center={center} \
                        &zoom={self.zoom}&size=256x256&maptype=satellite&key={api_key}"
                
                # Adds tile to row
                tile.append(self.retreiveTiles(url))
            
            # Adds row of tiles to column list
            tiles.append(tile)
        return tiles
    
    def getTileLimits(self):
        """ Calculates the number of tiles needed """
        x1, y1 = self.latLonToTile(self.lat1, self.lon1, self.zoom)
        x2, y2 = self.latLonToTile(self.lat2, self.lon2, self.zoom)
        return x1, y1, x2, y2
    
    def retreiveTiles(self, url):
        """
        Requests image from google maps API
        
        Parameter url: the url used for pulling google maps images
        """
        response = requests.get(url)
        if response.status_code == 200:
            image_array = np.frombuffer(response.content, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        else:
            print(f"Error: Failed to retrieve the image. Status code: {response.status_code}")
        return image
    
    def latLonToTile(self, lat, lon, zoom):
        """
        Converts latitude and longitude to (x,y)
        
        Parameter lat: latitude
        
        Parameter lon: longitude

        Parameter zoom: zoom level of the image
        """
        lat_rad = math.radians(lat)

        # Calculates the number of tiles, n
        n = 2.0 ** zoom
        xtile = (lon + 180.0) / 360.0 * n
        ytile = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return int(xtile), int(ytile)
    
    def tileToLatLon(self, x, y, zoom):
        """
        Converts (x,y) to latitude and longitude
        
        Parameter lat: latitude
        
        Parameter lon: longitude

        Parameter zoom: zoom level of the image
        """

        # Calculates the number of tiles, n
        n = 2.0 ** zoom
        lon_deg = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / n)))
        lat_deg = math.degrees(lat_rad)
        return str(lat_deg) + ', ' + str(lon_deg)