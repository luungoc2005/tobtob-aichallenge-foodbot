import requests
from flask import Flask
from flask_socketio import SocketIO
from pyzbar.pyzbar import decode
from PIL import Image
import requests
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tobtobsecret'

socketio = SocketIO(app)

@socketio.on('connection')
def connection(data):
    print('1 client connected')

@socketio.on('message')
def message(data):
    print('Data received')
    
    dataObj = json.loads(data)
    print('Loaded')

    img = Image.open(requests.get(dataObj['data'], stream=True).raw)
    print('Img loaded')

    # print(decode(img))
    decoded = decode(img)
    print('Img decoded')
    print(len(decoded))

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=4321)
    socketio.run(app, port=4321)

    
