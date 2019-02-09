#!/usr/bin/python
"""Main Script"""
import time
import i2c_interface
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

temp_sens = i2c_interface.temperature_sensor()
temp_sens.humidity_temp_set()
h = temp_sens.humidity_get()
t = temp_sens.temp_get()

def mqtt_pub(message):
    publish.single("IC.embedded/benchpsu",
    payload=message, 
    qos=2, 
    retain=False, 
    hostname="test.mosquitto.org",
    port=8884, 
    client_id="", 
    keepalive=60, 
    will=None, 
    auth=None, 
    tls={'ca_certs':"mosquitto.org.crt", 'certfile': "client.crt", 'keyfile': "client.key"},
    protocol=mqtt.MQTTv311, 
    transport="tcp")
    time.sleep(0.2)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))
    if str(msg.payload.decode("utf-8")) == "geegeeez":
        mqtt_pub("h" + str(h))
        mqtt_pub("t" + str(t))       

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org", port=8884)
client.subscribe("IC.embedded/benchpsu/#")
client.loop_start()

