import logging
import yaml
from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class MQTTConfig:
    host: str
    username: str
    password: str
    sensor_base_topic: str
    cover_base_topic: str
    util_base_topic: str = ''


@dataclass
class ServoChannelConfig:
    status: str
    servo_type: str
    servo_details: dict

    def check_config(self):
        """
        Checks required values are in the config
        :return: None
        """
        if self.servo_type != 'continuous_hacked':
            raise NotImplementedError('Only `continuous_hacked` servo type is currently supported')
        if self.servo_type == 'continuous_hacked':
            assert 'stationary_degrees' in self.servo_details
            assert 'open_degrees' in self.servo_details
            assert 'close_degrees' in self.servo_details
            assert 'open_time' in self.servo_details
            assert 'close_time' in self.servo_details


@dataclass
class Config:
    path: str
    mqtt: MQTTConfig
    all_servo_channels: int
    servo_channels: Dict[int, ServoChannelConfig]

    @classmethod
    def read_current_config(cls, config_path):
        with open(config_path) as c:
            logging.info(f'Attempting to read servo config from {config_path}')
            config = yaml.load(c, Loader=yaml.FullLoader)
        config['servo_channels'] = {k: ServoChannelConfig(**v) for k, v in config['servo_channels'].items()}
        config['mqtt'] = MQTTConfig(**config['mqtt'])
        config['path'] = config_path
        return cls(**config)

    def check_config(self):
        """
        Checks required values are in the config
        :return: None
        """
        assert self.servo_channels
        for channel, config in self.servo_channels.items():
            config.check_config()

    def write_current_config(self):
        dict_config = asdict(self)
        del dict_config['path']
        with open(self.path, 'w') as c:
            yaml.dump(dict_config, c, default_flow_style=False, allow_unicode=True)
