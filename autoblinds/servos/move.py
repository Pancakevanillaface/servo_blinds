from adafruit_servokit import ServoKit
import time
import argparse
import os
from datetime import datetime

from autoblinds.servos.ServosController import ServosController


def move_servo(channels, channel, movement, servo_details):
    kit = ServoKit(channels=channels)
    stationary, period = servo_details
    kit.servo[channel].angle = movement
    time.sleep(period)
    kit.servo[channel].angle = stationary


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Move the servo')

    arg_parser.add_argument('-c',
                            '--config',
                            help='Path to config',
                            required=False,
                            default=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                 'servos_config.yml'))
    arg_parser.add_argument('-ch',
                            '--channel',
                            help='Servo Channel',
                            required=True)
    arg_parser.add_argument('-m',
                            '--movement',
                            help='Whether to perform open or close movement',
                            choices=['open', 'close'],
                            required=True)

    args = vars(arg_parser.parse_args())

    servos_controller = ServosController(args['config'])
    if servos_controller.config['AUTO']:
        # move_servo(servos_controller.config['ALL_CHANNELS'],
        #            args['channel'],
        #            args['movement'],
        #            servos_controller.config[args['channel']]['SERVO_DETAILS'])
        file = open('{}.txt'.format(datetime.now().strftime('%s')), 'w')
        file.write('{}'.format(str(datetime.now())))
        file.close()
