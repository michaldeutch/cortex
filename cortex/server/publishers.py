import logging
import threading
from collections import defaultdict

import pika as pika

from ..utils.impl_store import ImplementationStore
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class Publisher:
    impl_store = ImplementationStore()

    def __init__(self, url):
        self.url = urlparse(url)
        self.impl = self.impl_store.get_impl(self.url.scheme)(self.url)

    def __enter__(self):
        return self.impl

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.impl.close()

    @impl_store.implementation('rabbitmq')
    class RabbitMQPublisher:
        def __init__(self, url):
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=url.hostname, port=url.port))
            logger.info(f'opened connection={self.connection}')
            self.channels = defaultdict(self.create_channel)

        def publish(self, message):
            channel = self.channels[threading.get_ident()]
            try:
                channel.basic_publish(exchange='thoughts', routing_key='',
                                      body=message)
                logger.debug(f'rabbitMQ publisher published message, '
                            f'id={threading.get_ident()}')
            except Exception as err:
                logger.error(f'failed to publish message={message}, '
                             f'channel={channel}', err)

        def create_channel(self):
            channel = self.connection.channel()
            channel.exchange_declare(exchange='thoughts',
                                     exchange_type='fanout')
            return channel

        def close(self):
            self.connection.close()
