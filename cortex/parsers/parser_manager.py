import inspect
import json
import logging
import pkgutil
from urllib.parse import urlparse

from . import parsers
from ..utils.rabbit_util.consumer import RabbitConsumer
from ..utils.rabbit_util.publisher import RabbitPublisher

logger = logging.getLogger(__name__)


class ParserManager:
    _parsers = {}

    def __init__(self):
        self._load_parsers()

    def _load_parsers(self):
        for loader, module_name, is_pkg in pkgutil.walk_packages(
                parsers.__path__):
            if is_pkg:
                continue
            module = loader.find_module(module_name).load_module(module_name)
            for name, val in module.__dict__.items():
                if not hasattr(val, 'field'):
                    continue
                if inspect.isclass(val) and name.endswith('Parser'):
                    self._parsers[val.field] = val().parse
                if inspect.isfunction(val) and name.startswith('parse_'):
                    self._parsers[val.field] = val

    def run_parser(self, name, data):
        if name not in self._parsers:
            logger.error(f'parsers {name} does not exists. Existing '
                         f'parsers= {self._parsers.keys()}')
            return ''
        parser = ParserManager._parsers[name]
        message = json.loads(data)
        if 'user' in message:
            return ''  # no parsers uses user message
        try:
            res = parser(message['snapshot'][name])
            if not res:
                return ''
            return json.dumps({
                'user_id': message['user_id'],
                'content': json.dumps(res),
                'timestamp': message['snapshot']['datetime']
            })
        except Exception as err:
            logger.error(f'parser {name} failed to parse message {message}',
                         err)
            return ''

    def run(self, name, url):
        def rabbit_run():
            publisher = RabbitPublisher(url, exchange='parsers',
                                        exchange_type='topic')
            snap_consumer = RabbitConsumer(url, exchange='thoughts',
                                           exchange_type='fanout')

            def callback(routing_key, body):
                try:
                    message = self.run_parser(name, body)
                    if message != '':
                        publisher.publish(routing_key=f'parser.{name}',
                                          body=message)
                        print(f'published message={message}')
                    return True
                except Exception as err:
                    logger.error(f'failed to publish message to parser='
                                 f'{name}', err)
                    return False

            snap_consumer.consume(callback)
            snap_consumer.close()
            publisher.close()

        if urlparse(url).scheme == 'rabbitmq':
            rabbit_run()
