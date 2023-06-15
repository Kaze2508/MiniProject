from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from bokeh.plotting import figure, output_file, show, save
from bokeh.embed import components
from bokeh.io import show
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
import pandas as pd
import sqlite3

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = '8UfmqqhmM4rC04D0mU4gfocqPDluQ93OR9Y5n5fZXxrOrUEBDwIIKKXpb8HR6AvL'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0

topic = '/topic/subtopic'
mqtt = Mqtt(app)
# db = client["mqtt"]
# collection = db["messages"]

# df = pd.DataFrame(list(collection.find()))

# # Create an output file for the chart
# output_file("line_chart.html")

# # Create a figure object for the chart
# p = figure(x_axis_type="datetime", title="MQTT Messages")

# # Add a line glyph to the figure with the data from the DataFrame
# p.line(x=df["topic"], y=df["payload"], line_width=2)

# # Show the chart in a web browser
# show(p)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt.subscribe(topic) # subscribe topic
        mqtt.publish(topic, 'Hello')
    else:
        print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))

# @app.route('/publish', methods=['POST'])
# def publish():
#     data = request.get_json()
#     mqtt_client.publish(topic, data['message'])
#     return jsonify(data)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

