#!/usr/bin/env python
import board
import busio
import json

# define i2c bus
i2c = busio.I2C(board.SCL, board.SDA)
# import adc board library
import adafruit_ads1x15.ads1115 as ADS
# import AnalogIn library
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c)

flow = AnalogIn(ads, ADS.P0)
air_q = AnalogIn(ads, ADS.P1)

flag = True
while flag:
	count = 0
	totalsum_flow = 0
	totalsum_air_q = 0
	while count <= 10:
		count += 1
		this_flow_voltage = flow.voltage
		if this_flow_voltage > 0.7:
			this_flow = (this_flow_voltage - 0.5) * 0.75
		else:
			this_flow = ((this_flow_voltage - 0.7) * 2.25 / 1.3) + 0.75
		totalsum_flow += this_flow
		totalsum_air_q += air_q.voltage
		if count == 10:
			totalsum_flow /= 10
			totalsum_air_q /= 10
			count = 0
			print("Air flow= ",totalsum_flow, " ", "Air quality= ",totalsum_air_q)