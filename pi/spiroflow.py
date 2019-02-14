#!/usr/bin/python3
"""Main Script"""
import time
from i2c_interface import TemperatureSensor, AirflowSensor
from mqtt_client import MQTTClient
from halo import Halo
import logging

HOST = "test.mosquitto.org"
PORT = 8884
TOPIC = "IC.embedded/benchpsu"

def main():
    # Initialize sensors
    temperature_sensor = TemperatureSensor()
    airflow_sensor = AirflowSensor()
    # Initialize MQTT client
    loader = Halo(spinner="bouncingBar", text="Initializing MQTT Broker")
    loader.start()
    mqtt_client = MQTTClient(HOST, PORT, TOPIC)
    loader.stop_and_persist()
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
