from flask import Flask, render_template
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'mqtt.flespi.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = '8UfmqqhmM4rC04D0mU4gfocqPDluQ93OR9Y5n5fZXxrOrUEBDwIIKKXpb8HR6AvL'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_REFRESH_TIME'] = 1.0

topic = 'topic/subtopic'
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(topic) # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode()
    )
    print('Received message on topic: {topic} with payload: {payload}'.format(**data))

@app.route('/publish', methods=['POST'])
def publish():
    data = request.get_json()
    mqtt_client.publish(topic, data['message'])
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

