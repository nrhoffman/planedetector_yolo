import cv2
import numpy as np
import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from imageprocessing import ImageProcessing
from tilecreator import TileCreator

load_dotenv()
#Set up Flask:
app = Flask(__name__)
#Set up Flask to bypass CORS:
cors = CORS(app)

@app.route("/getapi", methods=["GET"])
def getApi():
    api_key = os.getenv('API_KEY')
    return jsonify(api_key)

@app.route("/getplanes/<lat1>/<lon1>/<lat2>/<lon2>", methods=["GET"])
def getPlanes(lat1, lon1, lat2, lon2):
    tilecreator = TileCreator(float(lat1), float(lon1), float(lat2), float(lon2))

    stitched_image_ratio, stitched_image = ImageProcessing(tilecreator)

    cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
    if stitched_image_ratio >= 1.00:
        width = 1080
        height = int(1080 / stitched_image_ratio)
    else:
        width = int(1080 * stitched_image_ratio)
        height = 1080

    cv2.resizeWindow("Live", width, height)

    cv2.imshow('Live', np.array(stitched_image))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return jsonify("Success")

if __name__ == "__main__": 
   app.run(debug=True)