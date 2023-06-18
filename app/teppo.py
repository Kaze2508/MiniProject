from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask import jsonify
import sqlite3
import json
from bokeh.embed import components
from bokeh.plotting import figure
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'eco7k4WNUKZYNP2SxQmcxDP5SN3n8qBcrP7BHTdrs0d3F3L0JV14pE05fRid8Idp'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0

socketio = SocketIO(app,cors_allowed_origins="*")
mqtt = Mqtt(app)
topic = '/data'

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt.subscribe(topic) # subscribe topic
       mqtt.publish('28')

   else:
       print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_message(client, userdata, msg):
    data = dict(
        topic=msg.topic,
        payload=msg.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))
    payload = msg.payload.decode('utf-8')
    temperature = float(msg.payload.decode())
    temperature_data.append(temperature)
    socketio.emit('new_temperature', {'temperature': temperature})

def bacu():
    # print("Generating random sensor values")
    while True:
        temperature_value = random.randint(20, 40) # Random temperature between 20 and 40
        humidity_value = random.randint(40, 70) # Random humidity between 40 and 70
        print(temperature_value)
        print(humidity_value)
        socketio.emit('updateSensorData', {'humidity': humidity_value ,'temperature': temperature_value, "date": get_current_datetime()})
        socketio.sleep(10)

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

@socketio.on('connect')
def on_connect():
    socketio.emit('chart_data', {'temperature_data': temperature_data})

@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    socketio.start_background_task(bacu)
    socketio.run(app)