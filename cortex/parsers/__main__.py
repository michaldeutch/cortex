import sys
import logging
import click

from .parser_manager import ParserManager

logger = logging.getLogger(__name__)


@click.command()
@click.argument('parser_name', type=str)
@click.argument('raw_input', type=str)
def parse(parser_name, raw_input):
    print(ParserManager().run_parser(parser_name, raw_input))


@click.command()
@click.argument('parser_name', type=str)
@click.argument('message_queue', type=str)
def parse_to_queue(parser_name, message_queue):
    ParserManager().run(parser_name, message_queue)


if __name__ == '__main__':
    try:
        if sys.argv[1] == 'parse':
            parse(sys.argv[2:])
        elif sys.argv[1] == 'run-parser':
            parse_to_queue(sys.argv[2:])
        else:
            print('TRY: python -m cortex.parsers parse/run-parser --help')
    except Exception as error:
        logger.error('parsers main failed', error)
        print(f'An error occurred while running parser, {error}')
        sys.exit(1)
