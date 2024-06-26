import click

from . import __version__
from . import config_controller
from . import exp_sequence_controller


@click.command()
@click.version_option(version=__version__)
def main():
    """qlicS"""

    # Whole user dialogue prepping the configuration before the setup sequence.
    # This will also include loading defaults or saved forms

    config_controller.setup_sequence()

    exp_sequence_controller.create_and_run_sim()
