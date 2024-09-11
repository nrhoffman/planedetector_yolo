import cv2
import math
import numpy as np
import os
import requests

class TileCreator():
    def __init__(self, lat1, lon1, lat2, lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.zoom = 16
        self.tiles = self.generateTiles()
    
    def generateTiles(self):
        api_key = os.getenv('API_KEY')
        x1, y1, x2, y2 = self.getTileCount(self.lat1, self.lon1, self.lat2, self.lon2, self.zoom)
        tiles = []
        for y in range(y1, y2 + 1):
            tile = []
            for x in range(x1, x2 + 1):
                center = self.tileToLatLon(x, y, self.zoom)
                url = f"https://maps.googleapis.com/maps/api/staticmap?center={center}&zoom={self.zoom}&size=256x256&maptype=satellite&key={api_key}"
                tile.append(self.retreiveTiles(url))
            tiles.append(tile)
        return tiles
    
    def getTileCount(self, lat1, lon1, lat2, lon2, zoom):
        x1, y1 = self.latLonToTile(lat1, lon1, zoom)
        x2, y2 = self.latLonToTile(lat2, lon2, zoom)
        return x1, y1, x2, y2
    
    def retreiveTiles(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            image_array = np.frombuffer(response.content, dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        else:
            print(f"Error: Failed to retrieve the image. Status code: {response.status_code}")
        
        return image
    
    def latLonToTile(self, lat, lon, zoom):
        lat_rad = math.radians(lat)
        n = 2.0 ** zoom
        xtile = (lon + 180.0) / 360.0 * n
        ytile = (1.0 - math.log(math.tan(lat_rad) + 1.0 / math.cos(lat_rad)) / math.pi) / 2.0 * n
        return int(xtile), int(ytile)
    
    def tileToLatLon(self, x, y, zoom):
        n = 2.0 ** zoom
        lon_deg = x / n * 360.0 - 180.0
        lat_rad = math.atan(math.sinh(math.pi * (1.0 - 2.0 * y / n)))
        lat_deg = math.degrees(lat_rad)
        return str(lat_deg) + ', ' + str(lon_deg)