import yaml
import logging
import servoblinds.util.cron as cron


class ServosController:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}
        self.read_current_config()
        self.check_config()

    def read_current_config(self):
        with open(self.config_path) as c:
            logging.info('Attempting to read servo config from {}'.format(self.config_path))
            self.config = yaml.load(c, Loader=yaml.FullLoader)

    def check_config(self):
        """
        Checks required values are in the config
        :return: None
        """
        assert 'ALL_CHANNELS' in self.config
        for key in self.extract_servo_channels():
            assert 'stationary_degrees' in self.config[key]
            assert 'open_degrees' in self.config[key]
            assert 'close_degrees' in self.config[key]
            assert 'open_time' in self.config[key]
            assert 'close_time' in self.config[key]

    def extract_servo_channels(self):
        return [key for key in self.config if isinstance(key, int)]

    def update_auto(self, bool_value):
        """
        :param bool_value: whether the blinds are in an auto state or not
        :return:
        """
        self.config['AUTO'] = bool_value
        self.write_current_config()

    def update_state(self, channel, i):
        """
        :param channel: channel for the servo
        :param i: 0 or 1
        :return:
        """
        self.config[channel]['STATUS'] = float(i)
        self.write_current_config()

    def check_state(self, channel, i):
        """
        Checks for updates in the config.
        :return:
        """
        return self.config[channel]['STATUS'] == float(i)

    def schedule_servo_cronjobs(self):
        """
        Schedules jobs for the next week and a job to schedule more jobs
        :return:
        """
        cron.clear_crontab()
        for i in self.extract_servo_channels():
            cron.schedule_cron_jobs(self.config['LAT'],
                                    self.config['LON'],
                                    self.config_path,
                                    i,
                                    self.config[i])
        cron.schedule_final_cron_job(self.config_path)

    def write_current_config(self):
        with open(self.config_path, 'w') as c:
            yaml.dump(self.config, c, default_flow_style=False, allow_unicode=True)

