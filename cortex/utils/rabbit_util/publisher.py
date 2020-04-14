from urllib.parse import urlparse

import pika


class RabbitChannelPublisher:
    def __init__(self, connection, exchange, exchange_type):
        self.exchange = exchange
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type=exchange_type)

    def publish(self, routing_key, body):
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=routing_key, body=body)


class RabbitPublisher:
    def __init__(self, url, exchange, exchange_type='topic'):
        self.url = urlparse(url)
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = self.publisher_channel = None
        self._connect()

    def publish(self, routing_key, body):
        try:
            self.publisher_channel.publish(routing_key, body)
        except Exception:
            self._connect()
            self.publisher_channel.publish(routing_key, body)

    def close(self):
        try:
            self.connection.close()
        except Exception:
            pass

    def _connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.url.hostname,
                                      port=self.url.port))
        self.publisher_channel = RabbitChannelPublisher(self.connection,
                                                        self.exchange,
                                                        self.exchange_type)

