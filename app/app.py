from flask import Flask, render_template
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mybroker.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'user'
app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0
mqtt = Mqtt(app)

@app.route('/')
def index():
    return render_template('index.html')

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('home/mytopic')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )

if __name__ == '__main__':
    app.run(debug=True)

