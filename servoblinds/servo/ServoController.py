import time
import logging
from servoblinds.config import Config
from adafruit_servokit import ServoKit


class ServoController:
    def __init__(self, config: Config):
        self.config = config

    def move(self, movement):
        """
        Moves servo
        :param movement: open, close
        :return: None
        """
        if movement == 'open':
            new_state = 0.0
        elif movement == 'close':
            new_state = 1.0
        else:
            raise NotImplementedError('Movement can only be to `open` or `close`')

        if self.is_state(new_state):
            logging.warning('Already in requested state')
        else:
            kit = ServoKit(channels=self.config.all_servo_channels)
            for channel, servo in self.config.servo_channels.items():
                kit.servo[channel].angle = servo.servo_details['{}_degrees'.format(movement)]
                time.sleep(servo.servo_details['{}_time'.format(movement)])
                kit.servo[channel].angle = servo.servo_details['stationary_degrees']
            self.update_state(new_state)

    def update_state(self, state):
        """
        Updates states in config
        :param state:
        :return: None
        """
        for channel, servo in self.config.servo_channels.items():
            logging.info(f'Servo on channel {channel} updated to state: {state}')
            servo.status = state
        self.config.write_current_config()

    def is_state(self, state):
        """
        Checks for updates in the config
        :param state:
        :return: bool
        """
        states = [servo.status == state for channel, servo in self.config.servo_channels.items()]
        if any(states) and not all(states):
            _states = {channel: servo.status for channel, servo in self.config.servo_channels.items()}
            raise NotImplementedError(f'Servos are in varying states: {_states}')
        return all(states)
