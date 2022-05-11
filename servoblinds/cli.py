import click
import os
import yaml
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
from servoblinds.servo.ServosController import ServosController
from servoblinds.servo.move import override_servo
from servoblinds.util.cron import clear_crontab

@click.group()
def cli():
    pass


@cli.command('on')
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'config.yml'),
              help='Points to the config file defining servo')
def auto_on(config):
    """
    Starts automated blinds
    """
    servos_controller = ServosController(config)
    servos_controller.update_auto(True)
    servos_controller.write_current_config()
    servos_controller.schedule_servo_cronjobs()


@cli.command('off')
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'config.yml'),
              help='Points to the config file defining servo')
def auto_off(config):
    """
    Stops automated blinds
    """
    servos_controller = ServosController(config)
    servos_controller.update_auto(False)
    servos_controller.write_current_config()
    clear_crontab()


@cli.command('override')
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'config.yml'),
              help='Points to the config file defining servo')
@click.option('-ch', '--channel', required=False, type=float,
              default=None,
              help='You can select which servo to override, if not included overrides all servo')
def override(config, channel):
    """
    Changes current state
    """
    servos_controller = ServosController(config)
    if channel is None:
        for ch in servos_controller.extract_servo_channels():
            override_servo(ch, servos_controller)
    else:
        override_servo(channel, servos_controller)
    servos_controller.write_current_config()


@cli.command('stop')
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'config.yml'),
              help='Attempts to stop all servo, works if already calibrated')
def stop(config):
    """
    Attempts to stop all servo, works if already calibrated
    """
    from adafruit_servokit import ServoKit
    with open(config) as c:
        config = yaml.load(c, Loader=yaml.FullLoader)
    kit = ServoKit(channels=config['ALL_CHANNELS'])
    for key, val in config.items():
        if isinstance(key, int):
            try:
                kit.servo[key].angle = val['SERVO_DETAILS']['stationary_degrees']
            except KeyError:
                pass


if __name__ == '__main__':
    cli()