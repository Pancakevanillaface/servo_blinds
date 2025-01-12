import time
from abc import ABC
from servoblinds.config import ServoChannelConfig
from adafruit_servokit import ServoKit


class Servo(ABC):
    def __init__(self, channel, servo_config: ServoChannelConfig):
        # A servo that started as a positional servo, but was hacked to be continuous
        self.channel = channel
        self.servo_details = servo_config.servo_details

    def time_for_full_cycle(self, movement):
        return self.servo_details[f'{movement}_time']

    def move(self, kit: ServoKit, movement, t=None):
        raise NotImplementedError('Abstract class does not implement `move` method')

    def move_without_stopping(self, kit: ServoKit, movement):
        raise NotImplementedError('Abstract class does not implement `move_without_stopping` method')

    def stop(self, kit):
        raise NotImplementedError('Abstract class does not implement `stop` method')


class ContinuousHackedServo(Servo):
    def __init__(self, channel, servo_config):
        # A servo that started as a positional servo, but was hacked to be continuous
        super().__init__(channel, servo_config)

    def move(self, kit: ServoKit, movement, t=None):
        self.move_without_stopping(kit, movement)
        if t is None:
            time.sleep(self.time_for_full_cycle(movement))
        else:
            time.sleep(t)
        self.stop(kit)

    def move_without_stopping(self, kit: ServoKit, movement):
        kit.servo[self.channel].angle = self.servo_details['{}_degrees'.format(movement)]

    def stop(self, kit):
        kit.servo[self.channel].angle = self.servo_details['stationary_degrees']


class ContinuousServo(Servo):
    def __init__(self, channel, servo_config):
        super().__init__(channel, servo_config)

    @staticmethod
    def _movement_direction(movement):
        if movement == 'open':
            return 1
        elif movement == 'close':
            return -1
        else:
            raise RuntimeError(f'Movement: {movement} was not understood.')

    def move(self, kit: ServoKit, movement, t=None):
        self.move_without_stopping(kit, movement)
        if t is None:
            time.sleep(self.time_for_full_cycle(movement))
        else:
            time.sleep(t)
        self.stop(kit)

    def move_without_stopping(self, kit: ServoKit, movement):
        direction = self._movement_direction(movement)
        kit.continuous_servo[self.channel].throttle = direction * self.servo_details['throttle']

    def stop(self, kit):
        kit.continuous_servo[self.channel].throttle = 0
