##################################################
## MQTT Client Class
## Custom class wrapping Paho MQTT Client
##################################################
## Unlicensed
##################################################
## Author: benchPSU
## Copyright: Copyright 2019, Spiroflow
## Credits: [Mark Gee, Joel Yeow, Harvin Iriawan, Raymond Ooi]
## License: None
## Version: 1.0
## Maintainer: Mark Gee
## Status: active
##################################################

# Import relevant modules
import paho.mqtt.client as mqtt

# MQTT client class
class MQTTClient:
    """Class to handle MQTT connections and messages."""
    def __init__(self, host, port, topic):
        # Initialize with appropriate connection variables
        self.host = host
        self.port = port
        self.topic = topic

        # Flag to check if values are being recorded
        # This ensures values are not being constantly read,
        # reducing memory and power consumption.
        self.flow_flag = False

        # Initialize MQTT client
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.tls_set(ca_certs="./encryption/mosquitto.org.crt", certfile="./encryption/client.crt",keyfile="./encryption/client.key")
        
        # Force connection with while try loop
        # Ignores the buggy OSError exceptions thrown by mosquitto
        # Not the most elegant, but is sufficient to ensure connection
        connected = False
        while not connected:
            try:
                self.client.connect(host, port)
                connected = True
            except OSError:
                pass
        
        # Subscribe to topic and start polling asynchronously
        self.client.subscribe(self.topic)
        self.client.loop_start()
    

    # Define callbacks
    # Callback for when connection to broker successful
    def on_connect(self, client, userdata, rc):
        print("Connected with result code: "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.topic)

    # Callback for when message is received
    # Message handling defined here
    def on_message(self, client, userdata, msg):
        # Log message for debugging
        print(msg.topic+": "+str(msg.payload.decode("utf-8")))

        # If message indicates start/stop, change flow flag
        # as necessary
        if str(msg.payload.decode("utf-8")) == "start":
            self.flow_flag = True
        elif str(msg.payload.decode("utf-8")) == "stop":
            self.flow_flag = False

    # Callback for when message is published
    def on_publish(self, client, userdata, mid):
        # Log message for debugging
        print("Data published: " + mid)
        pass

    # Callback for when topic is subscribed to
    def on_subscribe(self, client,userdata, mid, granted_qos):
        print("Subscribed to " + mid)
        