from adafruit_servokit import ServoKit
import time
import argparse
import os
from datetime import datetime

from autoblinds.servos.ServosController import ServosController


def move_servo(channels, channel, movement, servo_details):
    kit = ServoKit(channels=channels)
    kit.servo[channel].angle = servo_details['{}_degrees'.format(movement)]
    time.sleep(servo_details['{}_time'.format(movement)])
    kit.servo[channel].angle = servo_details['stationary_degrees']


def override_servo_and_update_status(channel, servos_controller):
    if servos_controller.config[channel]['STATUS'] == 0:
        move_servo(servos_controller.config['ALL_CHANNELS'],
                   channel, 'close',
                   servos_controller.config[channel]['SERVO_DETAILS'])
        servos_controller.update_state(channel, 1)
    elif servos_controller.config[channel]['STATUS'] == 1:
        move_servo(servos_controller.config['ALL_CHANNELS'],
                   channel, 'open',
                   servos_controller.config[channel]['SERVO_DETAILS'])
        servos_controller.update_state(channel, 0)


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
    if args['movement'] == 'open':
        if (servos_controller.config['AUTO']) and (servos_controller.config[args['channel']]['STATUS'] == 1):
            move_servo(servos_controller.config['ALL_CHANNELS'],
                       args['channel'],
                       args['movement'],
                       servos_controller.config[args['channel']]['SERVO_DETAILS'])
            servos_controller.config[args['channel']]['STATUS'] = 0
    elif args['movement'] == 'close':
        if (servos_controller.config['AUTO']) and (servos_controller.config[args['channel']]['STATUS'] == 0):
            move_servo(servos_controller.config['ALL_CHANNELS'],
                       args['channel'],
                       args['movement'],
                       servos_controller.config[args['channel']]['SERVO_DETAILS'])
            servos_controller.config[args['channel']]['STATUS'] = 1
