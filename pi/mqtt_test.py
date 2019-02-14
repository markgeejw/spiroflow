import paho.mqtt.client as mqtt

HOST = "test.mosquitto.org"
PORT = 8884
TOPIC = "IC.embedded/benchpsu"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(TOPIC)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
# client.tls_set(ca_certs="./encryption/mosquitto.org.crt", certfile="./encryption/client.crt",keyfile="./encryption/client.key")
connected = False
while not connected:
    try:
        client.connect(HOST, PORT, 60)
        connected = True
    except:
        pass

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()