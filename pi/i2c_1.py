#!/usr/bin/python
from smbus2 import SMBusWrapper
import time

def run_adc():
	with SMBusWrapper(1) as bus:
		data_temperature = bus.read_i2c_block_data(0x40, 0xE3, 2)
		data_hum = bus.read_i2c_block_data(0x40, 0xE5, 2)

		# Convert the data
		tempC = ((data_temperature[0] * 256 + data_temperature[1]) * 175.72 / 65536.0) - 46.85
		hum = ((data_hum[0] * 256 + data_hum[1]) * 125 / 65536.0) - 6

		# Output data to screen
		print("Temp (digital): %d" %tempC)
		print("Humidity (digital): %d" %hum)
		return [tempC, hum]