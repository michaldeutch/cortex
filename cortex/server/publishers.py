import logging
import threading
from collections import defaultdict

import pika as pika

from utils.impl_store import ImplementationStore
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
            self.channels = defaultdict(self.create_channel)

        def publish(self, message):
            channel = self.channels[threading.get_ident()]
            channel.basic_publish(exchange='', routing_key='thoughts',
                                  body=message)
            logger.debug(f'rabbitMQ publisher published message, '
                         f'id={threading.get_ident()}')

        def create_channel(self):
            channel = self.connection.channel()
            channel.queue_declare(queue='thoughts')
            return channel

        def close(self):
            self.connection.close()
