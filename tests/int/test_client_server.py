import time
from threading import Thread

import pytest

from cortex.client import upload_sample
from cortex.server import run_server

messages = []


def test_client_upload(web_server, host, port, mind_file):
    upload_sample(host=host, port=port, path=str(mind_file))
    time.sleep(1)
    assert len(messages) == 2


@pytest.fixture
def web_server(host, port):
    def publish(message):
        messages.append(message)

    thread = Thread(target=run_server, args=(host, port, publish))
    thread.daemon = True
    thread.start()
    time.sleep(1)





