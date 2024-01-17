from flask import Flask, render_template, request, jsonify
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

app = Flask(__name__)

sensorData = {
              "/Temperature" : 0,
              "/Humidity" : 0
              }

mqtt_broker_ip = "broker.emqx.io"  

def on_message(client, userdata, msg):
    # Access sensorData as global
    global sensorData
    # Get topic from message and save it in topic
    topic = msg.topic
    # Decode the payload and save in payload variable
    payload = msg.payload.decode('utf-8')
    # Set key by topic in sensorData and save payload in it
    sensorData[topic] = payload
    print("Mqtt Data: ", msg.payload.decode('utf-8'),  msg.topic)

mqtt_client = mqtt.Client()
mqtt_client.on_message = on_message
mqtt_client.connect(mqtt_broker_ip, 1883, 60)
mqtt_client.subscribe("/Temperature")
mqtt_client.subscribe("/Humidity")
mqtt_client.loop_start()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/lightControl', methods=['POST'])
def lightControl():
    print("/lightControl is called")

@app.route("/getSensorData", methods=['POST'])
def getSensorData():
    return jsonify(sensorData)


if __name__ == '__main__':
    app.run(debug=True)
