from adafruit_servokit import ServoKit
import time


def calibrate_servo(channels, channel):
    """
    Finds the stationary point and how long it takes to operate the servo
    :return: SERVO_DETAILS:
    """
    kit = ServoKit(channels=channels)
    servo_details = {}

    # find a stationary degree for the servo
    is_stationary = 'n'
    stationary_degrees = 80
    while is_stationary != 'y':
        kit.servo[channel].angle = stationary_degrees
        is_stationary = input('Is the servo stationary? Answer only y or n')
        stationary_degrees += 1
    servo_details['stationary_degrees'] = stationary_degrees

    # find the open/close directions for the servo
    completely_finished = 'n'
    while completely_finished != 'y':
        kit.servo[channel].angle = 180
        direction = input('Check the direction of the servo. Is is spinning in'
                          'the direction to open or close the blind/curtain? '
                          'Answer only o for open or c for close.')
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
        kit.servo[channel].angle = stationary_degrees

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
            kit.servo[channel].angle = stationary_degrees
            is_closed = input('Is the blind/curtain in the close position?'
                              'Answer only y or n.')
        kit.servo[channel].angle = servo_details['open_degrees']
        time.sleep(period)
        kit.servo[channel].angle = stationary_degrees
        completely_finished = input('Has the blind/curtain returned to the open position?'
                                    'Answer only y or n.')

    servo_details['close_time'] = period
    servo_details['open_time'] = period


def has_calibrated_servo_details(SERVO_DETAILS):
    details = {'stationary_degrees', 'open_time', 'close_time', 'open_degrees', 'close_degrees'}
    if SERVO_DETAILS == None:
        return False
    elif details & set(SERVO_DETAILS) == details:
        return True
    else:
        return False