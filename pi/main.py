#!/usr/bin/python3
##################################################
## Main Script
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
import time
from i2c_interface.i2c_interface import TemperatureHumiditySensor, AirflowSensor
from mqtt_client.mqtt_client import MQTTClient

# Define connection variables
HOST = "test.mosquitto.org"
PORT = 8884
TOPIC = "IC.embedded/benchpsu"

def main():
    # Initialize sensors
    temperature_humidity_sensor = TemperatureHumiditySensor()
    airflow_sensor = AirflowSensor()
    # Initialize MQTT client
    mqtt_client = MQTTClient(HOST, PORT, TOPIC)
    print("Connected to MQTT Broker")

    # Poll in a continuous loop for data
    while True:
        # Check if data is being requested from UI
        if mqtt_client.flow_flag:
            # Send command to sensor to read the humidity then temperature
            temperature_humidity_sensor.humidity_temp_set()
            # Retrieve values of temperature, humidity, air flow
            h = temperature_humidity_sensor.humidity_get()
            t = temperature_humidity_sensor.temp_get()
            f = airflow_sensor.airflow_get()

            # Push messages in a simple string format
            mqtt_client.client.publish(TOPIC,'f'+str(f) + ' t' + str(t) + ' h' + str(h),2)
            time.sleep(0.1)
        # Else, do nothing
        else:
            time.sleep(0.1)
    
if __name__ == "__main__":
    main()
