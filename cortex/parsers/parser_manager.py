import inspect
import json
import pkgutil
from urllib.parse import urlparse

import pika

from . import parsers


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
            raise RuntimeError(f'parser {name} does not exists. Existing '
                               f'parsers= {self._parsers.keys()}')
        parser = ParserManager._parsers[name]
        message = json.loads(data)
        if message.user:
            return ''  # no parser uses user message
        return json.dumps({
            'user_id': data.user_id,
            'content': parser(message.snapshot[name]),
            'timestamp': message.snapshot.datetime
        })

    def run(self, name, url):

        def rabbit_run():
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=url.hostname, port=url.port))
            consumer_channel = connection.channel()
            publisher_channel = connection.channel()
            consumer_channel.exchange_declare(exchange='thoughts',
                                              exchange_type='fanout')
            publisher_channel.exchange_declare(exchange='parsers',
                                               exchange_type='topic')

            result = consumer_channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue

            consumer_channel.queue_bind(exchange='thoughts', queue=queue_name)

            def callback(ch, method, properties, body):
                publisher_channel.basic_publish(
                    exchange='parsers', routing_key=name, body=self.run_parser(
                        name, body))

            consumer_channel.basic_consume(
                queue=queue_name, on_message_callback=callback, auto_ack=True)
            consumer_channel.start_consuming()

        url = urlparse(url)
        if url.scheme == 'rabbitmq':
            rabbit_run()
