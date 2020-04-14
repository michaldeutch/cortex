from urllib.parse import urlparse

import pika


class RabbitChannelConsumer:
    def __init__(self, connection, exchange, exchange_type):
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.channel = connection.channel()
        self.channel.basic_qos(prefetch_count=5)
        self.channel.exchange_declare(exchange=exchange,
                                      exchange_type=exchange_type)
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.queue_name = result.method.queue

    def consume(self, callback, *routing_keys):
        self._bind(*routing_keys)
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=
                                   self._get_callback_wrapper(callback))
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def _get_callback_wrapper(self, callback):
        def callback_wrapper(ch, method, properties, body):
            success = callback(method.routing_key, body)
            if success:
                self.channel.basic_ack(method.delivery_tag)
            else:
                self.channel.basic_nack(method.delivery_tag)
        return callback_wrapper

    def _bind(self, *routing_keys):
        if self.exchange_type != 'topic':
            self.channel.queue_bind(exchange=self.exchange,
                                    queue=self.queue_name)
        else:
            for routing_key in routing_keys:
                self.channel.queue_bind(exchange=self.exchange,
                                        queue=self.queue_name,
                                        routing_key=routing_key)


class RabbitConsumer:
    def __init__(self, url, exchange, exchange_type='topic'):
        self.url = urlparse(url)
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = self.consumer_channel = None
        self._connect()

    def consume(self, callback, *routing_keys):
        try:
            self.consumer_channel.consume(callback, *routing_keys)
        except Exception:
            self._connect()
            self.consumer_channel.publish(callback, *routing_keys)

    def close(self):
        try:
            self.connection.close()
        except Exception:
            pass

    def _connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.url.hostname,
                                      port=self.url.port))
        self.consumer_channel = RabbitChannelConsumer(self.connection,
                                                      self.exchange,
                                                      self.exchange_type)
