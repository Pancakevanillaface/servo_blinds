
def calibrate_servo():
    """
    Finds the stationary point and how long it takes to operate the servo
    :return: SERVO_DETAILS:
    """
    pass


def check_config(SERVO_DETAILS):
    details = {'stationary_degrees', 'open_time', 'close_time', 'open_degrees', 'close_degrees'}
    if details | set(SERVO_DETAILS) == details:
        return True
    else:
        return False