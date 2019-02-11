#!/usr/bin/python
"""2 classes for temperature and air flow"""
from smbus2 import SMBus
from smbus2 import SMBusWrapper
from smbus2 import i2c_msg
import time

#TEMP_ADDRESS = 0x40
#WRITE_HUMIDITY_ADDRESS = 0xE5
#WRITE_TEMPERATURE_ADDRESS = 0xE3
class temperature_sensor:
    """My class to handle the readings from the SI7021 temp humid sensor
    """
    def __init__(self):
        self.address = 0x40
        self.humidityCommand = 0xF5
        self.tempCommand = 0xE0
        self.temp_value = None
        self.humidity_value = None

    def humidity_temp_set(self):
        """Sends command to read humidity. Then reads humidity with a pause between the two bytes.
        Temperature then reads as a temp reading is taken by the sensor for compensation for humidity reading
        """
        #---HUMIDITY I2C WRITE READ---#
        with SMBusWrapper(1) as bus:
            self.humidity_write = i2c_msg.write(self.address,[self.humidityCommand])
            self.humidity_read = i2c_msg.read(self.address,2)
            bus.i2c_rdwr(self.humidity_write)
            time.sleep(0.25)
            bus.i2c_rdwr(self.humidity_read)

        #---TEMP I2C WRITE READ---#
        with SMBusWrapper(1) as bus:
            self.temp_write = i2c_msg.write(self.address,[self.tempCommand])
            self.temp_read = i2c_msg.read(self.address,2)
            bus.i2c_rdwr(self.temp_write)
            bus.i2c_rdwr(self.temp_read)

    def humidity_get(self):
        """Carries out the maths for the humidity reading and returns it in %
        """
        #---HUMIDITY VALUE EDITING---#
        humidity_byte_list = list(self.humidity_read)
        humidity_MSB = humidity_byte_list[0]
        humidity_LSB = humidity_byte_list[1]
        humidity_word = (humidity_MSB<<8) + humidity_LSB
        self.humidity_value = ((125.0*humidity_word)/65536.0) - 6
        return round(self.humidity_value,2)

    def temp_get(self):
        """Carries out the maths for the temperature reading and returns it in DegC
        """
        #---TEMPERATURE VALUE EDITIING---#
        temp_byte_list = list(self.temp_read)
        temp_MSB = temp_byte_list[0]
        temp_LSB = temp_byte_list[1]
        temp_word = (temp_MSB<<8) + temp_LSB
        self.temp_value = ((175.72*temp_word)/65536)-46.85
        return round(self.temp_value,2)

class airflow_sensor:
    def __init__(self):
        self.address = 0x48
        self.writeCommand = [0x84,0x83]

    def airflow_get(self):
        """Sends commmands to read airflow speed and process the data,returns airflow speed"""
        with SMBusWrapper(1) as bus:
            bus.write_i2c_block_data(self.address, 0x01, self.writeCommand)
            time.sleep(0.1)
            # Read two bytes from register
            raw_data_flow = bus.read_i2c_block_data(self.address, 0x00, 2)
        # Convert the data
        raw_adc_flow = raw_data_flow[0] * 256 + raw_data_flow[1]
        if raw_adc_flow > 32767:
            raw_adc_flow -= 65535
        data_flow_V = raw_adc_flow * 6.144 / 32767

        #convert voltage into air flow velocity
        data_flow = data_flow_V * 2.0 / 3.0
        return data_flow