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
from i2c_interface import TemperatureSensor, AirflowSensor
from mqtt_client import MQTTClient

# Define connection variables
HOST = "test.mosquitto.org"
PORT = 8884
TOPIC = "IC.embedded/benchpsu"

def main():
    # Initialize sensors
    temperature_sensor = TemperatureHumiditySensor()
    airflow_sensor = AirflowSensor()
    # Initialize MQTT client
    mqtt_client = MQTTClient(HOST, PORT, TOPIC)
    print("Connected to MQTT Broker")

    while True:
        if mqtt_client.flow_flag:
            temperature_sensor.humidity_temp_set()
            h = temperature_sensor.humidity_get()
            t = temperature_sensor.temp_get()
            f = airflow_sensor.airflow_get()

            mqtt_client.client.publish(TOPIC,'f'+str(f) + ' t' + str(t) + ' h' + str(h),2)
            time.sleep(0.1)
        else:
            time.sleep(0.1)
    
if __name__ == "__main__":
    main()
