from cortex.server.publishers import Publisher
import pytest


def test_publishers():
    with pytest.raises(Exception):
        with Publisher('rabbitmq://127.0.0.1:5762') as publisher:
            assert isinstance(publisher, Publisher.RabbitMQPublisher)
