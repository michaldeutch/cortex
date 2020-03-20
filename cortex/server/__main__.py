import sys
import logging
import click
from .server import run_server

logger = logging.getLogger(__name__)


@click.command()
@click.option('-h', '--host', type=str, help='Run server on this host',
              default='127.0.0.1')
@click.option('-p', '--port', type=int, help='Run server on this port',
              default=8000)
@click.argument('publish', type=str)
def main(host, port, publish):
    run_server(host, port, publish)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'run-server':
            main(sys.argv[2:])
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
