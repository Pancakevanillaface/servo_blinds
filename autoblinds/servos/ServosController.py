import yaml


class ServosController(object):
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = {}
        self.read_current_config()

    def read_current_config(self):
        with open(self.config_path) as c:
            self.config = yaml.load(c, Loader=yaml.FullLoader)

    def update_auto(self, bool_value):
        """
        :param bool_value: whether the blinds are in an auto state or not
        :return:
        """
        self.config['AUTO'] = bool_value
        self.write_current_config()

    def engage_servos(self):
        while self.config['AUTO']:
            pass

    def write_current_config(self):
        with open(self.config_path, 'w') as c:
            yaml.dump(self.config, c, default_flow_style=False, allow_unicode=True)

