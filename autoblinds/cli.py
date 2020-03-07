import click

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-a', '--auto',
              type=click.Choice(['start', 'stop'], case_sensitive=False),
              help='Starts/Stops automation of the blinds')
def cli(auto):
    """
    Starts or stops automated blinds
    :param auto:
    :return:
    """
    if auto == 'start':
        # takes care of lining up the sunrise/sunset process
        click.echo(auto)
    elif auto == 'stop':
        # will clear the line-up
        click.echo(auto)

if __name__ == '__main__':
    cli()