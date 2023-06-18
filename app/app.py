from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import paho.mqtt.client as mqtt
import random
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

temperature_data = []  # Store received temperature data
humidity_data = []  # Store received humidity data

# MQTT configuration
mqtt_broker = 'mqtt.flespi.io'
mqtt_port = 1883
mqtt_username = 'eco7k4WNUKZYNP2SxQmcxDP5SN3n8qBcrP7BHTdrs0d3F3L0JV14pE05fRid8Idp'
temperature_topic = '/temperature'
humidity_topic = '/humidity'

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              timestamp TEXT NOT NULL,
              topic TEXT NOT NULL,
              payload TEXT NOT NULL)''')
conn.commit()

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe([(temperature_topic, 0), (humidity_topic, 0)])

def on_message(client, userdata, msg):
    topic = msg.topic
    if topic == temperature_topic:
        temperature = float(msg.payload.decode())
        random_offset = random.uniform(-1, 1)
        temperature += random_offset
        temperature_data.append(temperature)
        print('Temperature:', temperature)
        socketio.emit('new_temperature', {'temperature': temperature})
    elif topic == humidity_topic:
        humidity = float(msg.payload.decode())
        random_typo = random.uniform(-1, 1)
        humidity += random_typo
        humidity_data.append(humidity)
        print('Humidity:', humidity)
        socketio.emit('new_humidity', {'humidity': humidity})

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
    print('Temperature Data:', temperature_data)
    print('Humidity Data:', humidity_data)
    socketio.emit('chart_data', {'temperature_data': temperature_data, 'humidity_data': humidity_data})

# Background thread to start MQTT client
mqtt_thread = Thread(target=mqtt_thread)
mqtt_thread.start()

if __name__ == '__main__':
    app.run(host='192.168.0.156', port=5000, debug=True, threaded=False)
    socketio.run(app)