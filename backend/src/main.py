import base64
import cv2
import logging
import json
import numpy as np
import os
import redis
import time
from dotenv import load_dotenv
from flask import Flask, jsonify, Response
from flask_cors import CORS
from imageprocessing import ImageProcessing
from tilecreator import TileCreator

load_dotenv()
#Set up Flask:
app = Flask(__name__)
#Set up Flask to bypass CORS on the frontend service:
cors = CORS(app,
            resources={r"/api/*": {"origins": "http://frontend"}})
#Connect to redis server
r_conn = redis.Redis(host='redis', port=6379, db=0)

@app.route("/api/getapi", methods=["GET"])
def getApi():
    api_key = os.getenv('API_KEY')
    return jsonify(api_key)

@app.route("/api/getplanes/<lat1>/<lon1>/<lat2>/<lon2>", methods=["GET"])
def getPlanes(lat1, lon1, lat2, lon2):
    tilecreator = TileCreator(r_conn, float(lat1), float(lon1), float(lat2), float(lon2))

    stitched_image, num_of_planes = ImageProcessing(r_conn, tilecreator)

    # Encode the image to Base64
    _, buffer = cv2.imencode('.jpg', np.array(stitched_image))
    image_base64 = base64.b64encode(buffer).decode('utf-8')

    data = {
        "Status": 'Complete'
    }
    r_conn.hmset("Update", data) 

    return jsonify({
        'numberOfPlanes': num_of_planes,
        'image': image_base64
    })

@app.route("/api/getprogress", methods=["GET"])
def getProgress():
    return Response(event_stream(),
                    mimetype="text/event-stream")

def event_stream():
    data = {"Status": "Pending"}
    json_data = json.dumps(data)
    yield f"data: {json_data}\n\n"
    time.sleep(2)
    Update = r_conn.hgetall("Update")
    Update = {key.decode('utf-8'): value.decode('utf-8') for key, value in Update.items()}
    while Update['Status'] != "Complete":
        data = {
            "Status": Update['Status'],
            "Type": Update['Type'],
            "Value": Update['Value'],
            "Total": Update['Total']
        }
        json_data = json.dumps(data)
        yield f"data: {json_data}\n\n"
        time.sleep(1)
        Update = r_conn.hgetall("Update")
        Update = {key.decode('utf-8'): value.decode('utf-8') for key, value in Update.items()}
    data = {
        "Status": Update['Status'],
        "Type": Update['Type'],
        "Value": Update['Value'],
        "Total": Update['Total']
    }
    json_data = json.dumps(data)
    yield f"data: {json_data}\n\n"

if __name__ == "__main__": 
   app.run(debug=False)