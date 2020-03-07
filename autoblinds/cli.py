import click
import os

from autoblinds.servos.ServosController import ServosController


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-a', '--auto',
              type=click.Choice(['start', 'stop'], case_sensitive=False),
              help='Starts/Stops automation of the blinds')
@click.option('-c', '--config',
              required=False, type=str,
              default=os.path.join(os.path.dirname(__file__), 'servos_config.yml'),
              help='Points to the config file defining servos')
def cli(auto, config):
    """
    Starts or stops automated blinds
    :param auto:
    :return:
    """
    if auto == 'start':
        # takes care of the sunrise/sunset process
        servos_controller = ServosController(config)
        servos_controller.update_auto(True)
    elif auto == 'stop':
        # will end the auto state
        servos_controller = ServosController(config)
        servos_controller.update_auto(False)

if __name__ == '__main__':
    cli()