import board
import busio
import adafruit_vcnl4040


class SensorVNCN4040(object):
    def __init__(self, channel_config):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_vcnl4040.VCNL4040(self.i2c)
        self.config = channel_config['SENSOR_DETAILS']

    def whithin_closed_range(self):
        if self.sensor.light < self.config['open']['light']:
            return True
        return False

