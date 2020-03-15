from adafruit_servokit import ServoKit
import time


def is_calibrated(key, servo_details):
    if (key not in servo_details):
        return True
    elif (servo_details[key] is None):
        return True
    else:
        return False


def calibrate_servo(channels, channel, servo_details=None):
    """
    Finds the stationary point and how long it takes to operate the servo
    :return: SERVO_DETAILS:
    """
    kit = ServoKit(channels=channels)
    if servo_details is None:
        servo_details = {}

    # find a stationary degree for the servo
    if is_calibrated('stationary_degrees', servo_details):
        is_stationary = 'n'
        stationary_degrees = 80
        while is_stationary != 'y':
            kit.servo[channel].angle = stationary_degrees
            is_stationary = input('Is the servo on channel {} stationary? '
                                  'Answer only y or n: '.format(channel))
            stationary_degrees += 1
        servo_details['stationary_degrees'] = stationary_degrees

    # find the open/close directions for the servo
    if is_calibrated('open_degrees', servo_details) or is_calibrated('close_degrees', servo_details):
        completely_finished = 'n'
        while completely_finished != 'y':
            kit.servo[channel].angle = 180
            direction = input('Check the direction of the servo on channel {}. Is is spinning in '
                              'the direction to open or close the blind/curtain? '
                              'Answer only o for open or c for close. '.format(channel))
            if direction=='o':
                servo_details['open_degrees'] = 180
                servo_details['close_degrees'] = 0
                completely_finished = 'y'
            elif direction=='c':
                servo_details['open_degrees'] = 0
                servo_details['close_degrees'] = 180
                completely_finished =  'y'
            else:
                print('You\'ve screwed up. Try again.')
            kit.servo[channel].angle = servo_details['stationary_degrees']

    # find how long it takes to operate the servo to open/close
    if is_calibrated('open_time', servo_details) or is_calibrated('close_time', servo_details):
        period = 0
        increase_delta = 3
        print('Readjust the blind/curtain to the open position.')
        completely_finished = 'n'
        while completely_finished != 'y':
            is_closed = 'n'
            while is_closed != 'y':
                period += increase_delta
                kit.servo[channel].angle = servo_details['close_degrees']
                time.sleep(increase_delta)
                kit.servo[channel].angle = servo_details['stationary_degrees']
                is_closed = input('Is the blind/curtain in the close position? '
                                  'Answer only y or n. ')
            kit.servo[channel].angle = servo_details['open_degrees']
            time.sleep(period)
            kit.servo[channel].angle = servo_details['stationary_degrees']
            completely_finished = input('Has the blind/curtain returned to the open position? '
                                        'Answer only y or n.')

        servo_details['close_time'] = period
        servo_details['open_time'] = period

    return servo_details


def has_calibrated_servo_details(SERVO_DETAILS):
    details = {'stationary_degrees', 'open_time', 'close_time', 'open_degrees', 'close_degrees'}
    if SERVO_DETAILS == None:
        return False
    elif details & set(SERVO_DETAILS) == details:
        return True
    else:
        return False