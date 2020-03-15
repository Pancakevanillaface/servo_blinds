import click
import os

from autoblinds.servos.ServosController import ServosController


@click.group()
def cli():
    pass


@cli.group()
def auto():
    pass


@auto.command('on')
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'servos_config.yml'),
              help='Points to the config file defining servos')
def auto_on(config):
    """
    Starts automated blinds
    """
    servos_controller = ServosController(config)
    servos_controller.update_auto(True)
    servos_controller.write_current_config()
    servos_controller.schedule_servo_cronjobs()


@auto.command('off')
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'servos_config.yml'),
              help='Points to the config file defining servos')
def auto_off(config):
    """
    Stops automated blinds
    """
    servos_controller = ServosController(config)
    servos_controller.update_auto(False)
    servos_controller.write_current_config()


@cli.group()
def override():
    pass


@override.command()
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'servos_config.yml'),
              help='Points to the config file defining servos')
def override_auto():
    """
    Changes current state
    """
    pass


@cli.group()
def calibrate():
    pass


@override.command()
@calibrate.option('-c', '--config', required=False, type=str,
                  default=os.path.join(os.path.dirname(__file__), 'servos_config.yml'),
                  help='Calibrates servos')
def calibrate_servo(config):
    """
    Calibrates servos
    """
    servos_controller = ServosController(config)
    servos_controller.calibrate()
    servos_controller.write_current_config()


if __name__ == '__main__':
    cli()