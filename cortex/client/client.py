import logging
import click

logger = logging.getLogger(__name__)


@click.command()
@click.option('-h', '--host', type=str, help='Upload sample to this host',
              default='127.0.0.1')
@click.option('-p', '--port', type=int, help='Upload sample to this port',
              default=8000)
@click.argument('path', type=str)
def upload_sample(host, port, path):
    print(f'upload_sample, host={host}, port={port}, path={path}')


