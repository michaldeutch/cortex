import json
import logging
from threading import Thread
from urllib.parse import urlparse

from cortex.utils.db_util import Database
from cortex.utils.rabbit_util.consumer import RabbitConsumer

logger = logging.getLogger(__name__)


class Saver:
    parsers = ['parser.feelings', 'parser.pose', 'parser.color_image',
               'parser.depth_image']

    def __init__(self, database_url, database=Database):
        self.url = database_url
        self.database = database

    def save(self, parser, data):
        with self.database(self.url) as db:
            self.save_parser_result(db, parser, data)

    def run(self, url):
        with Database(self.url) as db:
            def rabbit_run():
                parsers = RabbitConsumer(url, 'parsers', 'topic')
                user = RabbitConsumer(url, 'thoughts', 'fanout')

                def parser_callback(routing_key, body):
                    try:
                        parser_name = routing_key.split('.')[1]
                        self.save_parser_result(db, parser_name, body)
                        return True
                    except Exception as err:
                        logger.error(f'failed to save message={body} '
                                     f'coming from {routing_key}', err)
                        return False

                def user_callback(routing_key, body):
                    try:
                        message = json.loads(body)
                        if 'user' in message:
                            db.store_user(message['user_id'], message[
                                'user'])
                        return True
                    except Exception as err:
                        logger.error(f'failed to save user message='
                                     f'{body}', err)
                        return False
                try:
                    user_exec = Thread(target=user.consume, args=(
                        user_callback,))
                    user_exec.start()
                    parsers.consume(parser_callback, *self.parsers)
                except KeyboardInterrupt:
                    parsers.close()
                    user.close()

            if urlparse(url).scheme == 'rabbitmq':
                rabbit_run()

    @staticmethod
    def save_parser_result(db, parser, data):
        obj = json.loads(data)
        db.store_parser_result(obj['user_id'], obj['timestamp'], parser,
                               obj['content'])
