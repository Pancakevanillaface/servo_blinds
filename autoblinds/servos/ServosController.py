import yaml
import time

import autoblinds.util.cron as cron
import autoblinds.servos.calibrate as calibrate


class ServosController(object):
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}
        self.read_current_config()
        self.check_config()

    def read_current_config(self):
        with open(self.config_path) as c:
            self.config = yaml.load(c, Loader=yaml.FullLoader)

    def check_config(self):
        """
        Checks required values are in the config and gives defaults
        :return:
        """
        assert 'AUTO' in self.config
        assert 'LAT' in self.config
        assert 'LON' in self.config
        assert 'ALL_CHANNELS' in self.config
        for key in self.extract_servo_channels():
            assert 'STATUS' in self.config[key]
            assert 0.0 <= self.config[key]['STATUS'] <= 1.0

            if not 'SUNRISE_BUFFER' in self.config[key]:
                self.config[key]['SUNRISE_BUFFER'] = 0
            if not 'SUNSET_BUFFER' in self.config[key]:
                self.config[key]['SUNSET_BUFFER'] = 0

            if 'SERVO_DETAILS' in self.config[key]:
                if not calibrate.has_calibrated_servo_details(self.config[key]['SERVO_DETAILS']):
                    self.calibrate()
            else:
                self.calibrate()

    def extract_servo_channels(self):
        return [key for key in self.config if isinstance(key, int)]

    def update_auto(self, bool_value):
        """
        :param bool_value: whether the blinds are in an auto state or not
        :return:
        """
        self.config['AUTO'] = bool_value
        self.write_current_config()

    def check_state_and_auto(self):
        """
        Checks for updates in the config.
        :return:
        """
        pass

    def calibrate(self):
        for key in self.extract_servo_channels():
            self.config[key]['SERVO_DETAILS'] = calibrate.calibrate_servo(
                self.config['ALL_CHANNELS'], key, self.config[key]['SERVO_DETAILS']
            )

    def schedule_servo_cronjobs(self):
        """
        Schedules jobs for the next week and a job to schedule more jobs
        :return:
        """
        for i in self.extract_servo_channels():
            cron.schedule_cron_jobs(self.config['LAT'], self.config['LON'], self.config_path, i)
        cron.schedule_final_cron_job(self.config_path)

    def write_current_config(self):
        with open(self.config_path, 'w') as c:
            yaml.dump(self.config, c, default_flow_style=False, allow_unicode=True)

