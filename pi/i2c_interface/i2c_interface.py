#!/usr/bin/python3
##################################################
## I2C Interface Class
## Defines the interface for communicating with
## air flow sensor and temperature humidity sensor
## using I2C
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
from smbus2 import SMBus
from smbus2 import SMBusWrapper
from smbus2 import i2c_msg
import time

class TemperatureHumiditySensor:
    """Class to handle the readings from the SI7021 temp humid sensor
    """
    def __init__(self):
        # I2C address
        self.address = 0x40
        # Commands for I2C
        self.humidityCommand = 0xF5
        self.tempCommand = 0xE0
        # Initialize temperature and humidity readings
        self.temp_value = None
        self.humidity_value = None

    def humidity_temp_set(self):
        """Sends command to read humidity. Then reads humidity with a pause between the two bytes.
        Temperature then reads as a temp reading is taken by the sensor for compensation for humidity reading
        """
        # Reading values for humidity
        with SMBusWrapper(1) as bus:
            # Write command to start reading humidity
            self.humidity_write = i2c_msg.write(self.address,[self.humidityCommand])
            # Read command to actually read humidity
            self.humidity_read = i2c_msg.read(self.address,2)  
            # Execute with a pause                         
            bus.i2c_rdwr(self.humidity_write)
            time.sleep(0.25)
            bus.i2c_rdwr(self.humidity_read)

        #Reading values for temperature
        with SMBusWrapper(1) as bus:
            # Write command to start reading temperature
            self.temp_write = i2c_msg.write(self.address,[self.tempCommand])
            # Read command to actually read temperature
            self.temp_read = i2c_msg.read(self.address,2)
            # Execute
            bus.i2c_rdwr(self.temp_write)
            bus.i2c_rdwr(self.temp_read)

    def humidity_get(self):
        """Carries out the maths for the humidity reading and returns it in %
        """
        # Read humidity value
        humidity_byte_list = list(self.humidity_read)
        humidity_MSB = humidity_byte_list[0]
        humidity_LSB = humidity_byte_list[1]
        humidity_word = (humidity_MSB<<8) + humidity_LSB
        # Calculate relative humidity
        self.humidity_value = ((125.0*humidity_word)/65536.0) - 6
        return round(self.humidity_value,2)

    def temp_get(self):
        """Carries out the maths for the temperature reading and returns it in DegC
        """
        # Read temperature value
        temp_byte_list = list(self.temp_read)
        temp_MSB = temp_byte_list[0]
        temp_LSB = temp_byte_list[1]
        temp_word = (temp_MSB<<8) + temp_LSB
        # Calculate temperature in Celsius
        self.temp_value = ((175.72*temp_word)/65536)-46.85
        return round(self.temp_value,2)

class AirflowSensor:
    """Class to handle the readings from the D6F-V air flow sensor, wired with
    the ADS1115 ADC."""
    def __init__(self):
        # I2C addresses
        self.address = 0x48
        self.writeCommand = [0x84,0x83]

    def airflow_get(self):
        """Sends commmands to read airflow speed and process the data,returns airflow speed"""
        with SMBusWrapper(1) as bus:
            # Write command to read airflow
            bus.write_i2c_block_data(self.address, 0x01, self.writeCommand)
            time.sleep(0.1)
            # Read airflow data as 2 bytes from register
            raw_data_flow = bus.read_i2c_block_data(self.address, 0x00, 2)
        # Convert the data into voltage
        raw_adc_flow = raw_data_flow[0] * 256 + raw_data_flow[1]
        if raw_adc_flow > 32767:
            raw_adc_flow -= 65535
        data_flow_V = raw_adc_flow * 6.144 / 32767

        # Convert voltage into air flow velocity
        data_flow = data_flow_V * 2.0 / 3.0
        return data_flow