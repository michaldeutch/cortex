import multiprocessing
import struct
import time

import pytest
from flask import Flask
from cortex.client.reader import Reader
from tests.conftest import USER_ID

app = Flask(__name__)


@pytest.fixture
def web_server(host, port):

    def run_web():
        @app.route('/user/<user_id>', methods=['POST'])
        def post(user_id):
            assert user_id == str(USER_ID)
            return '200'
        app.run(host, port)

    process = multiprocessing.Process(target=run_web)
    process.start()
    time.sleep(1)
    try:
        yield
    finally:
        process.terminate()
        process.join()


@pytest.fixture
def reader(mind_file):
    yield Reader(str(mind_file), 'proto')
