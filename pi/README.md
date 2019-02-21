# Spiroflow Main Code
This is the code that runs off the pi zero. It uses a MQTT client in a pubsub architecture for sending and receiving data to and from the cloud with SSL encryption. I2C interface is used for reading values off the sensors (and ADC).

## Components Used
- Pi Zero W
- Si7021 Temperature Humidity Sensor
- D6F-V Airflow Sensor
- ADS1115 Analog-to-Digital Convertor (ADC)

## Installing dependences
`pip install -r requirements.txt`

## Testing
Run in pi folder

`python3 tests/mqtt_test.py`

## Usage
`python3 main.py`