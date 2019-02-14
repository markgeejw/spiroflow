import paho.mqtt.client as mqtt
import halo

class MQTTClient:
    def __init__(self, host, port, topic):
        self.host = host
        self.port = port
        self.topic = topic
        self.flow_flag = False

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.tls_set(ca_certs="./encryption/mosquitto.org.crt", certfile="./encryption/client.crt",keyfile="./encryption/client.key")
        
        connected = False
        while not connected:
            try:
                self.client.connect(host, port)
                connected = True
            except:
                pass
        self.client.subscribe(self.topic)
        self.client.loop_start()
    

    # Define callbacks
    def on_connect(self, client, userdata, rc):
        print("Connected with result code: "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print(msg.topic+": "+str(msg.payload.decode("utf-8")))
        if str(msg.payload.decode("utf-8")) == "start":
            self.flow_flag = True
        elif str(msg.payload.decode("utf-8")) == "stop":
            self.flow_flag = False


    def on_publish(self, client, userdata, mid):
        print("Data published: " + mid)
        pass

    def on_subscribe(self, client,userdata, mid, granted_qos):
        print("Subscribed to " + mid)
        