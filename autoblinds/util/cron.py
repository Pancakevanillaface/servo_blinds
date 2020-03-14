import datetime
from astral.sun import sun
from astral import LocationInfo
from crontab import CronTab
import argparse

from autoblinds.servos.ServosController import ServosController


def schedule_cron_jobs(lat, lon):
    cron = CronTab(user=True)

    city = LocationInfo(name='', region='', timezone='', latitude=lat, longitude=lon)
    for i in range(1,8):
        date = datetime.datetime.now() + datetime.timedelta(days=i)
        s = sun(city.observer, date=date)
        print('')

        # s['sunrise']
        # s['sunset']

        if i == 7:
            pass


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='Schedules next jobs')

    arg_parser.add_argument('-c',
                            '--config',
                            help='Path to config',
                            required=True)

    args = vars(arg_parser.parse_args())

    servos_controller = ServosController(args['config'])
    if servos_controller.config['AUTO']:
        servos_controller.schedule_servo_cronjobs()
