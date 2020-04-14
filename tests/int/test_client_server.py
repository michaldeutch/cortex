import time
from threading import Thread

import pytest

from cortex.client import upload_sample
from cortex.server import run_server

messages = []


def test_client_upload(local_server, host, server_port, mind_file):
    upload_sample(host=host, port=server_port, path=str(mind_file))
    time.sleep(1)
    assert len(messages) == 2


@pytest.fixture
def local_server(host, server_port):
    def publish(message):
        messages.append(message)

    thread = Thread(target=run_server, args=(host, server_port, publish))
    thread.daemon = True
    thread.start()
    time.sleep(1)





