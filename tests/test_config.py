import os
import pytest
from servoblinds.config import Config, ServoChannelConfig, MQTTConfig


@pytest.fixture()
def sample_config_path():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'servoblinds', "sample_config.yml"))


def test_instantiating_config_from_yaml_results_in_expected_class_types(sample_config_path):
    config = Config.read_current_config(sample_config_path)
    assert isinstance(config, Config)
    assert isinstance(config.mqtt, MQTTConfig)
    assert isinstance(config.servo_channels[1], ServoChannelConfig)
