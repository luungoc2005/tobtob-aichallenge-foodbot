import requests
from flask import Flask
from flask_socketio import SocketIO
from pyzbar.pyzbar import decode
from PIL import Image
from pyzbar.pyzbar import ZBarSymbol
from io import BytesIO
import urllib.request
import traceback
import sys
import requests
import json
import math
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tobtobsecret'

socketio = SocketIO(app)

VIDEO_WIDTH = 344
VIDEO_HEIGHT = 260

def distance(x1, y1, x2, y2):
    return abs(x1 - y1) + abs(x2 - y2)

@socketio.on('connection')
def connection(data):
    print('1 client connected')

@socketio.on('message')
def message(data):
    try:
        print('Data received')

        dataObj = json.loads(data)
        # print('Loaded')

        # response = requests.get(dataObj['data'])
        
        # img = Image.open(BytesIO(response.content))
        response = urllib.request.urlopen(dataObj['data'])
        img = Image.open(response)
        # print('Img loaded')

        # print(decode(img))
        decoded = decode(img, symbols=[ZBarSymbol.QRCODE])
        print(len(decoded))
        if len(decoded) > 0:
            if len(decoded) == 1:
                socketio.emit('message', json.dumps({
                    'type': 'result',
                    'data': decoded[0].data
                }))
            else:
                distances = []
                prediction = dataObj['hand_prediction']

                x2_norm = float(prediction.bbox[0]) / float(VIDEO_WIDTH)
                y2_norm = float(prediction.bbox[1]) / float(VIDEO_HEIGHT)

                for decoded_item in decoded:
                    x1_norm = float(decoded_item.rect.left) / float(img.width)
                    y1_norm = float(decoded_item.rect.top) / float(img.height)

                    distances.push(distance(x1_norm, y1_norm, x2_norm, y2_norm))

                minIdx = np.argmin(distances)
                socketio.emit('message', json.dumps({
                    'type': 'result',
                    'data': decoded[minIdx].data
                }))
    
    except Exception:
        try:
            exc_info = sys.exc_info()

        finally:
            # Display the *original* exception
            traceback.print_exception(*exc_info)
            del exc_info

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=4321)
    socketio.run(app, port=5000, debug=True)

    
