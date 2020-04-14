import time

import pika
import pytest
import docker
import requests

from cortex.utils.serdes_util.serializers import Serializer
from tests.conftest import USER_ID

# TODO- not done
# def test_server_to_rabbit(user, consumer, host, port):
#     resp = requests.post(f'http://{host}:{port}/user/{USER_ID}',
#                          headers={'Content-Type': 'proto'},
#                          data=Serializer('proto').serialize(user))
#     def callback(ch, method, properties, body):
#         print(f'consumed a message!!!!!!!!! {body}')
#
#     time.sleep(20)
#     consumer.basic_get('thoughts', callback)
#     print('hahahah')


@pytest.fixture(scope='session')
def docker_rabbitmq():
    container = docker.from_env().containers.run("rabbitmq:3-management", detach=True, auto_remove=True, ports={5672: 5672, 15672: 15672})
    time.sleep(60)
    yield
    container.stop()


@pytest.fixture(scope='session')
def docker_server(docker_rabbitmq, port):
    container = docker.from_env().containers.run("cortex-server:latest", auto_remove=True, network_mode='host', detach=True)
    time.sleep(10)
    yield
    container.stop()


@pytest.fixture(scope='session')
def consumer():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672))
    channel = connection.channel()
    channel.queue_declare(queue='thoughts')

    yield channel
    channel.close()
    connection.close()
