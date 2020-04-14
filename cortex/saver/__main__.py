import sys
import logging
import click

from .saver import Saver

logger = logging.getLogger(__name__)


@click.command()
@click.option('-d', '--database', type=str, help='The database url', default='')
@click.argument('parser_topic', type=str)
@click.argument('parser_result', type=str)
def save(database_url, parser_topic, parser_result):
    saver = Saver(database_url)
    with open(parser_result, "r") as result:
        saver.save(parser_topic, result.read())


@click.command()
@click.argument('database_url', type=str)
@click.argument('message_queue_url', type=str)
def run_saver(database_url, message_queue_url):
    saver = Saver(database_url)
    saver.run(message_queue_url)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'save':
            save(sys.argv[2:])
        elif sys.argv[1] == 'run-saver':
            run_saver(sys.argv[2:])
        else:
            print('TRY: python -m cortex.saver save/run-saver --help')
    except Exception as error:
        logger.error('saver main failed', error)
        print(f'An error occurred while running saver, {error}')
        sys.exit(1)
