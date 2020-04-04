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
@click.argument('mind_path', type=str)
def main(host, port, mind_path):
    upload_sample(host, port, mind_path)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'upload-sample':
            main(sys.argv[2:])
        else:
            print('TRY: python -m cortex.client upload-sample --help')
    except Exception as error:
        logger.error('client main failed', error)
        print(f'An error occurred while running client, {error}')
        sys.exit(1)
