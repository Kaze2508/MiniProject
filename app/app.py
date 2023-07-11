from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import paho.mqtt.client as mqtt
import random
import sqlite3
from datetime import datetime
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

temperature_data = []  # Store received temperature data
humidity_data = []  # Store received humidity data
data = []

# MQTT configuration
mqtt_broker = 'mqtt.flespi.io'
mqtt_port = 1883
mqtt_username = 'eco7k4WNUKZYNP2SxQmcxDP5SN3n8qBcrP7BHTdrs0d3F3L0JV14pE05fRid8Idp'
temperature_topic = 'prediction/result'
humidity_topic = '/humidity'

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe([(temperature_topic, 0), (humidity_topic, 0)])

def on_message(client, userdata, msg):
    topic = msg.topic
    # temperature = msg.payload.decode()
    # socket.emit('new_temperature', {'temperature': temperature})
    # insert_data_to_db(timestamp, temperature, sensor_type)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if topic == temperature_topic:
        sensor_type = 'Temperature'
        # temperature = float(msg.payload.decode())
        temperature = msg.payload.decode()
        # random_offset = random.uniform(-1, 1)
        # temperature += random_offset
        # data.append((timestamp, temperature, sensor_type))
        print('Temperature:', temperature)
        socketio.emit('new_temperature', {'temperature': temperature})
        insert_data_to_db(timestamp, temperature, sensor_type)
    elif topic == humidity_topic:
        sensor_type = 'Humidity'
        humidity = float(msg.payload.decode())
        random_typo = random.uniform(-1, 1)
        humidity += random_typo
        data.append((timestamp, humidity, sensor_type))
        print('Humidity:', humidity)
        socketio.emit('new_humidity', {'humidity': humidity})
        insert_data_to_db(timestamp, humidity, sensor_type)         

def insert_data_to_db(timestamp, sensor_data, sensor_type):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO data (timestamp, sensor_data, sensor_type) VALUES (?, ?, ?)", (timestamp, sensor_data, sensor_type))
    conn.commit()
    conn.close()

def create_data_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS data
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            sensor_data REAL NOT NULL,
            sensor_type TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def mqtt_thread():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_username)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_port, 60)
   #  client.loop_forever()
    client.loop_start()

# Route to render the chart webpage
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Query data from the data table
    c.execute("SELECT * FROM data")
    data = c.fetchall()

    conn.close()

    return render_template('index.html', data=data)

@app.route('/my_route')
def my_route():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Query data from the data table
    c.execute("SELECT * FROM data")
    data = c.fetchall()

    conn.close()

    return render_template('database.html', data=data)

@app.route('/update_temp')
def update_temp():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT ROUND(sensor_data, 2) FROM data WHERE sensor_type='Temperature' ORDER BY id DESC LIMIT 1")
    temperature = c.fetchone()
    conn.close()
    if temperature:
        return str(temperature[0])
    else:
        return ""


@app.route('/update_humi')
def update_humi():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT ROUND(sensor_data, 2) FROM data WHERE sensor_type='Humidity' ORDER BY id DESC LIMIT 1")
    humidity = c.fetchone()
    conn.close()
    if humidity:
        return str(humidity[0])
    else:
        return ""
    
@app.route('/database')
def database():
    return render_template('database.html')

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
