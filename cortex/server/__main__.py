import sys
import logging
import click

from .publishers import Publisher
from .server import run_server

logger = logging.getLogger(__name__)


@click.command()
@click.option('-h', '--host', type=str, help='Run server on this host',
              default='127.0.0.1')
@click.option('-p', '--port', type=int, help='Run server on this port',
              default=8000)
@click.argument('publisher_url', type=str)
def main(host, port, publisher_url):
    with Publisher(publisher_url) as publisher:
        run_server(host, port, publisher.publish)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'run-server':
            main(sys.argv[2:])
        else:
            print('TRY: python -m cortex.server run-server --help')
    except Exception as error:
        logger.error('server main failed', error)
        print(f'An error occurred while running server, {error}')
        sys.exit(1)
