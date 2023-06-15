from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask import jsonify
import sqlite3
import json

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = '8UfmqqhmM4rC04D0mU4gfocqPDluQ93OR9Y5n5fZXxrOrUEBDwIIKKXpb8HR6AvL'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0

mqtt = Mqtt(app)
topic = '/topic/subtopic'

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS data
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              topic TEXT NOT NULL,
              payload TEXT NOT NULL)''')
conn.commit()
conn.close()

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe(topic)

# @mqtt.on_message()
# def handle_message(client, userdata, msg):
#     conn = sqlite3.connect('database.db')
#     c = conn.cursor()
#     c.execute("INSERT INTO data (topic, payload) VALUES (?,?)", (msg.topic, msg.payload))
#     conn.commit()
#     conn.close()

@mqtt.on_message()
def handle_message(client, userdata, msg):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    payload = msg.payload.decode('utf-8')
    c.execute("INSERT INTO data (topic, payload) VALUES (?,?)", (msg.topic, payload))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

@app.route('/my_route')
def my_route():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM data")
    data = c.fetchall()
    conn.close()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run()