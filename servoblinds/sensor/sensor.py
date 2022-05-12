import board
import busio
import adafruit_vcnl4040


class SensorVNCN4040:
    """
    https://learn.adafruit.com/adafruit-vcnl4040-proximity-sensor
    """
    def __init__(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vcnl4040.VCNL4040(self.i2c)

    @property
    def light(self):
        return self.sensor.light

    @property
    def proximity(self):
        return self.sensor.proximity

    @property
    def white(self):
        return self.sensor.white
