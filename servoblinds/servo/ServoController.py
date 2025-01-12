import logging
from servoblinds.config import Config
from servoblinds.servo.servo import *
from adafruit_servokit import ServoKit

SERVO_TYPE_MAP = {
    'continuous_hacked': ContinuousHackedServo,
    'continuous': ContinuousServo
}


class ServoController:
    def __init__(self, config: Config):
        self.config = config
        self.kit = ServoKit(channels=self.config.all_servo_channels)
        self.servos = {
            channel: SERVO_TYPE_MAP[servo.servo_type](channel, servo) for channel, servo in
            config.servo_channels.items()
        }
        self.movement_time = self.check_for_equal_movement_time()

    def check_for_equal_movement_time(self):
        movement_times = {'open': False, 'close': False}
        for movement in movement_times.keys():
            times = [servo.time_for_full_cycle(movement) for servo in self.servos.values()]
            if len(set(times)) == 1:
                movement_times[movement] = times[0]
        return movement_times

    def get_servo_on_channel(self, channel):
        return self.servos[channel]

    def _move(self, movement):
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
            raise NotImplementedError('Movement can only be `open` or `close`')

        if self.is_state(new_state):
            logging.warning('Already in requested state')
        else:
            servos = [self.get_servo_on_channel(channel) for channel, servo in self.config.servo_channels.items()]
            if self.movement_time[movement]:
                # all servos can move at the same time
                [servo.move_without_stopping(self.kit, movement) for servo in servos]
                time.sleep(self.movement_time[movement])
                [servo.stop(self.kit) for servo in servos]
            else:
                [servo.move(self.kit, movement) for servo in servos]
            self.update_state(new_state)

    def stop(self):
        logging.info('Stopping all servos')
        for channel, servo in self.config.servo_channels.items():
            self.get_servo_on_channel(channel).stop(self.kit)

    def open(self):
        logging.info('Opening all')
        self._move('open')

    def close(self):
        logging.info('Closing all')
        self._move('close')

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
