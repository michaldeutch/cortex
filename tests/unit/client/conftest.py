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


@pytest.fixture(scope='session')
def mind_file(tmp_path_factory):
    return tmp_path_factory.mktemp('mind_files').joinpath('test.mind')


@pytest.fixture
def reader(mind_file, user, snapshot):
    with mind_file.open('wb') as rp:
        serialize_to_file(rp, user)
        serialize_to_file(rp, snapshot)
    yield Reader(str(mind_file), 'proto')


def serialize_to_file(rp, entity):
    serialized_entity = entity.SerializeToString()
    rp.write(struct.pack('I', len(serialized_entity)))
    rp.write(serialized_entity)


@pytest.fixture
def host():
    return 'localhost'


@pytest.fixture
def port():
    return 7000
