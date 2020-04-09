import struct

import pytest
from cortex.utils.messages import cortex_pb2 as mind

USER_ID = 123


@pytest.fixture(scope='session')
def host():
    return 'localhost'


@pytest.fixture(scope='session')
def port():
    return 8000


@pytest.fixture(scope='session')
def mind_file(tmp_path_factory, user, snapshot):
    mind_file = tmp_path_factory.mktemp('mind_files').joinpath('test.mind')
    with mind_file.open('wb') as rp:
        serialize_to_file(rp, user)
        serialize_to_file(rp, snapshot)
    return mind_file


@pytest.fixture(scope='session')
def snapshot(color_image):
    translation = mind.Pose.Translation(x=1, y=1, z=1)
    rotation = mind.Pose.Rotation(x=2, y=2, z=2, w=2)
    pose = mind.Pose(translation=translation, rotation=rotation)
    depth_image = mind.DepthImage(width=20, height=30, data=[1.0, 1.1, 1.2])
    feelings = mind.Feelings(hunger=1, thirst=1, exhaustion=1, happiness=1)
    return mind.Snapshot(datetime=20200703, pose=pose,
                         color_image=color_image, depth_image=depth_image,
                         feelings=feelings)


@pytest.fixture(scope='session')
def color_image():
    RGB = (0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0)
    return mind.ColorImage(width=2, height=2, data=struct.pack('12B', *RGB))


@pytest.fixture(scope='session')
def user():
    return mind.User(user_id=USER_ID, username='michaldeutch', birthday=699746400)


def serialize_to_file(rp, entity):
    serialized_entity = entity.SerializeToString()
    rp.write(struct.pack('I', len(serialized_entity)))
    rp.write(serialized_entity)
