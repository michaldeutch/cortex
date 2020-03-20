import multiprocessing
import struct
import time

import pytest
from flask import Flask

from cortex.utils import cortex_pb2 as mind
from cortex.client.deserializers import ProtoDes
from cortex.client.reader import Reader

app = Flask(__name__)


@pytest.fixture
def web_server(host, port):

    def run_web():
        @app.route('/', methods=['POST'])
        def post():
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
    yield Reader(str(mind_file), ProtoDes())


@pytest.fixture
def snapshot():
    translation = mind.Pose.Translation(x=1, y=1, z=1)
    rotation = mind.Pose.Rotation(x=2, y=2, z=2, w=2)
    pose = mind.Pose(translation=translation, rotation=rotation)
    color_image = mind.ColorImage(width=20, height=30, data=b'color_data')
    depth_image = mind.DepthImage(width=20, height=30)
    feelings = mind.Feelings(hunger=1, thirst=1, exhaustion=1, happiness=1)
    return mind.Snapshot(datetime=20200703, pose=pose,
                         color_image=color_image, depth_image=depth_image,
                         feelings=feelings)


@pytest.fixture
def user():
    return mind.User(user_id=25, username='michaldeutch', birthday=699746400)


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
