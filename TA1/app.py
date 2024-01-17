from flask import Flask, render_template, request, jsonify
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

app = Flask(__name__)

sensorData = {
              "/Temperature" : 0,
              "/Humidity" : 0
              }

#  Create a mqtt_broker_ip to hold the broker IP
mqtt_broker_ip = "broker.emqx.io"  

# Define callback function on_message() for handling incoming MQTT messages with three parameter client, userdata, msg
def on_message(client, userdata, msg):
    print("Mqtt Data: ", msg.payload.decode('utf-8'),  msg.topic)

# Create an MQTT client instance
mqtt_client = mqtt.Client()
# Set the callback function for incoming messages
mqtt_client.on_message = on_message
# Connect to the MQTT broker
mqtt_client.connect(mqtt_broker_ip, 1883, 60)
# Subscribe to the desired MQTT topics
mqtt_client.subscribe("/Temperature")
mqtt_client.subscribe("/Humidity")
# Start the MQTT loop to listen for incoming messages
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
