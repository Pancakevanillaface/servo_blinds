# servo_blinds

Python code to control servos and send sensor data via MQTT and Home Assistant.

### Rough outline of my set-up:
1. Device controlling three [continuous rotation (hacked)](https://rookieelectronics.com/servohack/) servos and a sensor:
   - Raspberry Pi Zero W
   - [Adafruit 16-Channel PWM / Servo Bonnet for Raspberry Pi](https://www.adafruit.com/product/3416)
   - [Adafruit VCNL4040 Proximity Sensor](https://learn.adafruit.com/adafruit-vcnl4040-proximity-sensor) sensor
2. Separate HA server device, runs in a docker container

## Installation on device

My device uses a Raspberry Pi Zero W:

1. [Install MQTT on the Pi](https://randomnerdtutorials.com/how-to-install-mosquitto-broker-on-raspberry-pi/)
2. Install this code and dependencies (if you're using this pi for other things you may want to consider using a 
virtual environment for this). From the root directory of this repository:
    
        pip install -e .

## Home Assistant Setup

1. Install MQTT in your HA setup - [helpful youtube video](https://www.youtube.com/watch?v=dqTn-Gk4Qeo)
2. Add device(s) to your HA's `configuration.yaml` 
   - [how to add a simple switch](https://roelofjanelsinga.com/articles/how-to-create-switch-dashboard-home-assistant/)
   - [HA documentation on other MQTT device types](https://www.home-assistant.io/docs/mqtt/discovery/)

   This is what I added for my living room blinds and a light+proximity sensor which are operated by the same Raspberry
   Pi:




