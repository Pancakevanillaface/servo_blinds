import time
import argparse
import os
from datetime import datetime
from autoblinds.sensor.proximity import SensorVNCN4040
from adafruit_servokit import ServoKit
from autoblinds.servo.ServosController import ServosController


def move_servo(config, channel, movement):
    channels = config['ALL_CHANNELS']
    servo_details = config[channel]['SERVO_DETAILS']
    if movement == 'open':
        movement_int = 0
    elif movement == 'close':
        movement_int = 1
    else:
        raise NotImplementedError('Movement can only be to `open` or `close`')

    kit = ServoKit(channels=channels)
    kit.servo[channel].angle = servo_details['{}_degrees'.format(movement)]

    t = servo_details['{}_time'.format(movement)]
    if t != 'sensor':
        time.sleep(t)
    else:
        sensor = SensorVNCN4040(config[channel])
        while sensor.proximity_whithin_closed_range():
            time.sleep(0.3)

    kit.servo[channel].angle = servo_details['stationary_degrees']
    servos_controller.update_state(channel, movement_int)


def override_servo(channel, servos_controller):
    if servos_controller.check_state(channel, 0):
        move_servo(servos_controller.config, channel, 'close')
    elif servos_controller.check_state(channel, 1):
        move_servo(servos_controller, channel, 'open')


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
                            required=True,
                            type=int)
    arg_parser.add_argument('-m',
                            '--movement',
                            help='Whether to perform open or close movement',
                            choices=['open', 'close'],
                            required=True)

    args = vars(arg_parser.parse_args())

    servos_controller = ServosController(args['config'])
    if args['movement'] == 'open':
        if (servos_controller.config['AUTO']) and (servos_controller.check_state(args['channel'], 1)):
            move_servo(servos_controller.config,
                       args['channel'],
                       args['movement'])
    elif args['movement'] == 'close':
        if (servos_controller.config['AUTO']) and (servos_controller.check_state(args['channel'], 0)):
            move_servo(servos_controller.config,
                       args['channel'],
                       args['movement'])
