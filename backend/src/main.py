import base64
import cv2
import numpy as np
import os
import redis
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from imageprocessing import ImageProcessing
from tilecreator import TileCreator

load_dotenv()
#Set up Flask:
app = Flask(__name__)
#Set up Flask to bypass CORS on the frontend service:
cors = CORS(app,
            resources={r"/api/*": {"origins": "http://frontend"}})

@app.route("/api/getapi", methods=["GET"])
def getApi():
    api_key = os.getenv('API_KEY')
    return jsonify(api_key)

@app.route("/api/getplanes/<lat1>/<lon1>/<lat2>/<lon2>", methods=["GET"])
def getPlanes(lat1, lon1, lat2, lon2):
    tilecreator = TileCreator(float(lat1), float(lon1), float(lat2), float(lon2))

    stitched_image, num_of_planes = ImageProcessing(tilecreator)

    # Encode the image to Base64
    _, buffer = cv2.imencode('.jpg', np.array(stitched_image))
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        'numberOfPlanes': num_of_planes,
        'image': image_base64
    })

if __name__ == "__main__": 
   app.run(debug=False)