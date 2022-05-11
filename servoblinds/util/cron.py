import datetime
from astral.sun import sun
from astral import LocationInfo
from crontab import CronTab
import argparse
import os

import servoblinds.servo.ServosController as ServosController


def schedule_cron_jobs(lat, lon, config_path, channel, channel_config):
    path_to_source = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    cron = CronTab(user=True)

    city = LocationInfo(name='', region='', timezone='', latitude=lat, longitude=lon)
    for i in range(1,8):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        s = sun(city.observer, date=date)

        # s['sunrise']
        j = cron.new('python3 {} -c {} -ch {} -m open'.format(
            os.path.join(path_to_source, 'servo', 'move.py'), config_path, channel))
        j.setall(s['sunrise'] + datetime.timedelta(minutes=channel_config['SUNRISE_BUFFER']))

        # s['sunset']
        j = cron.new('python3 {} -c {} -ch {} -m close'.format(
            os.path.join(path_to_source, 'servo', 'move.py'), config_path, channel))
        j.setall(s['sunset'] + datetime.timedelta(minutes=channel_config['SUNSET_BUFFER']))

    cron.write(user=True)


def schedule_final_cron_job(config_path):
    path_to_source = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    date = datetime.datetime.now() + datetime.timedelta(days=7)
    cron = CronTab(user=True)
    j = cron.new('python3 {} -c {}'.format(
        os.path.join(path_to_source, 'util', 'cron.py'), config_path))
    j.setall(date)
    cron.write(user=True)


def clear_crontab():
    cron = CronTab(user=True)
    cron.remove_all()
    cron.write(user=True)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Schedules next jobs')

    arg_parser.add_argument('-c',
                            '--config',
                            help='Path to config',
                            required=False,
                            default=os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                 'servos_config.yml'))

    args = vars(arg_parser.parse_args())

    servos_controller = ServosController.ServosController(args['config'])
    if servos_controller.config['AUTO']:
        clear_crontab()
        servos_controller.schedule_servo_cronjobs()
    schedule_final_cron_job(args['config'])
