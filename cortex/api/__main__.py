from cortex.utils.db_util import Database
from .api_server import run_api_server
import sys
import logging
import click

logger = logging.getLogger(__name__)


@click.command()
@click.option('-h', '--host', type=str, help='Run server on this host',
              default='127.0.0.1')
@click.option('-p', '--port', type=int, help='Run server on this port',
              default=5000)
@click.option('-d', '--database', type=str, help='Access this db, should be '
                                                 'like mongodb://<ip>:<port>/')
def main(host, port, database):
    with Database(database) as db:
        run_api_server(host, port, db)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'run-server':
            main(sys.argv[2:])
        else:
            print('TRY: python -m cortex.api run-server --help')
    except Exception as error:
        logger.error('api main failed', error)
        print(f'An error occurred while running api, {error}')
        sys.exit(1)
