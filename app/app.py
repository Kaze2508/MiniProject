from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import paho.mqtt.client as mqtt
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

temperature_data = []  # Store received temperature data

# MQTT configuration
mqtt_broker = 'mqtt.flespi.io'
mqtt_port = 1883
mqtt_username = 'eco7k4WNUKZYNP2SxQmcxDP5SN3n8qBcrP7BHTdrs0d3F3L0JV14pE05fRid8Idp'
mqtt_topic = '/data'

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    temperature = float(msg.payload.decode())
    random_offset = random.uniform(-3, 3)  # Generate a random value between -3 and 3
    temperature += random_offset
    temperature_data.append(temperature)
    print(temperature)
    socketio.emit('new_temperature', {'temperature': temperature})

def mqtt_thread():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_username)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()

# Route to render the chart webpage
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(temperature_data)
    socketio.emit('chart_data', {'temperature_data': temperature_data})

# Background thread to start MQTT client
mqtt_thread = Thread(target=mqtt_thread)
mqtt_thread.start()

if __name__ == '__main__':
    socketio.run(app)