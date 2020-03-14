from adafruit_servokit import ServoKit
import time
import argparse

from autoblinds.servos.ServosController import ServosController


def move_servo(channels, channel, servo_details):
    kit = ServoKit(channels=channels)
    stationary, degrees, period = servo_details
    kit.servo[channel].angle = degrees
    time.sleep(period)
    kit.servo[channel].angle = stationary


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Move the servo')

    arg_parser.add_argument('-c',
                            '--config',
                            help='Path to config',
                            required=True)
    arg_parser.add_argument('-ch',
                            '--channel',
                            help='Servo Channel',
                            required=True)

    args = vars(arg_parser.parse_args())

    servos_controller = ServosController(args['config'])
    if servos_controller.config['AUTO']:
        move_servo(servos_controller.config['ALL_CHANNELS'],
                   args['channel'],
                   servos_controller.config[args['channel']]['SERVO_DETAILS'])
