#!/usr/bin/python
"""Main Script"""
import time
import i2c_interface
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe

"""initialise the 2 sensor objects"""
temp_sens = i2c_interface.temperature_sensor()

airflow_sens = i2c_interface.airflow_sensor()

"""not used for now"""
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

'''define callbacks'''
def on_connect(client, userdata, rc):
    if rc == 0:
        print("Connected with result code "+str(rc))
    else:
        print ("Bad connection return "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode("utf-8")))  

def on_publish(client,userdata,mid):
    print("data published = " + mid)
    pass

def on_subscribe(client,userdata,mid,granted_qos):
    print("subscribed to "+mid)

""" callbacks not used for now """
def on_th(client, userdata, message):
    print ("============publishing temperature & humidity data on callback============")
    while True:
        print("in while loop th")
        temp_sens.humidity_temp_set()
        h = temp_sens.humidity_get()
        t = temp_sens.temp_get()
        client.publish("IC.embedded/benchpsu", "h" + str(h),2)
        client.publish("IC.embedded/benchpsu", "t" + str(t),2)
        time.sleep(3)
def on_airflow(client, userdata, message):
    print ("============publishing airflow data on callback============")
    while True:
        print("in while loop airflow")
        a = airflow_sens.airflow_get()
        client.publish("IC.embedded/benchpsu","f" + str(a))
        time.sleep(0.1)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.on_subscribe = on_subscribe

msg = subscribe.simple("IC.embedded/benchpsu", hostname="test.mosquitto.org", port=8884,
    tls={'ca_certs':"mosquitto.org.crt", 'certfile': "client.crt", 'keyfile': "client.key"})
print(str(msg.payload.decode("utf-8")))



client.tls_set(ca_certs="mosquitto.org.crt", certfile="client.crt",keyfile="client.key")
client.connect("test.mosquitto.org", port=8884)
client.subscribe("IC.embedded/benchpsu/#")
client.loop_start()

while True:
    print("in the while loop sending all 3 sensor data")
    temp_sens.humidity_temp_set()
    h = temp_sens.humidity_get()
    t = temp_sens.temp_get()
    f = airflow_sens.airflow_get()

    print("about to send airflow")
    client.publish("IC.embedded/benchpsu",'f'+str(f) + ' t' + str(t) + ' h' + str(h),2)
    time.sleep(0.1)