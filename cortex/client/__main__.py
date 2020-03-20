from .client import upload_sample
import sys
import logging
import click

logger = logging.getLogger(__name__)


@click.command()
@click.option('-h', '--host', type=str, help='Upload sample to this host',
              default='127.0.0.1')
@click.option('-p', '--port', type=int, help='Upload sample to this port',
              default=8000)
@click.argument('path', type=str)
def main(host, port, path):
    upload_sample(host, port, path)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'upload-sample':
            main(sys.argv[2:])
    except Exception as error:
        logger.error(f'{error}')
        sys.exit(1)
