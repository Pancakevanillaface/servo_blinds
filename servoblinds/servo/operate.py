import os
import argparse
import logging
from servoblinds.servo.ServoController import ServoController
from servoblinds.config import Config
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Open/Close blinds without MQTT client')

    arg_parser.add_argument('-c',
                            '--config_path',
                            help='Path to config',
                            required=False,
                            default=os.path.join(os.path.dirname(__file__), 'sample_config.yml'))

    arg_parser.add_argument('-op',
                            '--operation',
                            help='Operation to perform',
                            required=True,
                            choices=['open', 'close'])

    args = vars(arg_parser.parse_args())
    config = Config.read_current_config(args['config_path'])
    sc = ServoController(config)

    operation = args['operation']
    if operation == 'open':
        sc.open()
    elif operation == 'close':
        sc.close()
