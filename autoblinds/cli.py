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
    servos_controller.engage_servos()


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


@cli.group()
def override():
    pass


@override.command()
@click.option('-c', '--config', required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'servos_config.yml'),
              help='Points to the config file defining servos')
def override_auto():
    pass


if __name__ == '__main__':
    cli()