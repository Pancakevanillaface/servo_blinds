import yaml
import time


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
        assert 'ALL_CHANNELS' in self.config
        if 'UPDATE_FREQUENCY' not in self.config:
            self.config['UPDATE_FREQUENCY'] = 10
        for key, val in self.config.items():
            if isinstance(key, int):
                assert 'STATUS' in val
                assert 0.0 <= val['STATUS'] <= 1.0

                assert 'ROTATIONS_TO_CLOSE' in val

                if not 'SUNRISE_BUFFER' in val:
                    self.config[key]['SUNRISE_BUFFER'] = 0
                if not 'SUNSET_BUFFER' in val:
                    self.config[key]['SUNSET_BUFFER'] = 0

    def update_auto(self, bool_value):
        """
        :param bool_value: whether the blinds are in an auto state or not
        :return:
        """
        self.config['AUTO'] = bool_value
        self.write_current_config()

    def engage_servos(self):
        while self.config['AUTO']:
            time.sleep(10*60*60)
            # todo add servos doing things
            self.read_current_config()
        exit()

    def write_current_config(self):
        with open(self.config_path, 'w') as c:
            yaml.dump(self.config, c, default_flow_style=False, allow_unicode=True)

