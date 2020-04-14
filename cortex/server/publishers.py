import logging
import threading

from cortex.utils.impl_util import ImplementationStore
from urllib.parse import urlparse

from cortex.utils.rabbit_util.publisher import RabbitPublisher

logger = logging.getLogger(__name__)


class Publisher:
    impl_store = ImplementationStore()

    def __init__(self, url):
        self.url = urlparse(url)
        self.impl = self.impl_store.get_impl(self.url.scheme)(url)

    def __enter__(self):
        return self.impl

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.impl.close()

    @impl_store.implementation('rabbitmq')
    class RabbitMQPublisher:
        def __init__(self, url):
            self.lock = threading.Lock()
            self.rabbit_publisher = RabbitPublisher(url, 'thoughts', 'fanout')
            self.cnt = 0

        def publish(self, message):
            with self.lock:
                self.cnt += 1
                try:
                    self.rabbit_publisher.publish(routing_key='', body=message)
                    logger.debug(f'rabbitMQ publisher published message, '
                                 f'id={threading.get_ident()}')
                    print(f'published {self.cnt} messages')
                except Exception as err:
                    logger.error(f'failed to publish message, error={err}')

        def close(self):
            self.rabbit_publisher.close()
