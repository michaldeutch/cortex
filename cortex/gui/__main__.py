import sys
import logging
import click

from cortex.gui import run_server

logger = logging.getLogger(__name__)


@click.command()
@click.option('-h', '--host', type=str, help='Run server on this host',
              default='127.0.0.1')
@click.option('-p', '--port', type=int, help='Run server on this port',
              default=8080)
@click.option('-H', '--api-host', type=str, help='Define the APIs host',
              default='127.0.0.1')
@click.option('-P', '--api-port', type=int, help='Define the APIs port',
              default=5000)
def main(host, port, api_host, api_port):
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'run-server':
            main(sys.argv[2:])
        else:
            print('TRY: python -m cortex.gui run-server --help')
    except Exception as error:
        logger.error('gui main failed', error)
        print(f'An error occurred while running gui, {error}')
        sys.exit(1)
