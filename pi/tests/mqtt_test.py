##################################################
## MQTT Test
## Ensures MQTT Broker can be connected to
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

# Import relevant modulesimport sys
import sys
sys.path.append("./mqtt_client")
import paho.mqtt.client as mqtt
from mqtt_client import MQTTClient

# Define connection variables
HOST = "test.mosquitto.org"
PORT = 8884
TOPIC = "IC.embedded/benchpsu"

client = MQTTClient(HOST, PORT, TOPIC)
print("MQTT test success!")