import struct
from collections import defaultdict

import pytest
from google.protobuf.json_format import MessageToJson

from cortex.utils.messages import cortex_pb2 as mind

USER_ID = 123


@pytest.fixture(scope='session')
def host():
    return 'localhost'


@pytest.fixture(scope='session')
def server_port():
    return 8000


@pytest.fixture(scope='session')
def api_port():
    return 5000


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
    return mind.User(user_id=USER_ID, username='michaldeutch',
                     birthday=699746400)


@pytest.fixture
def db(user, snapshot):
    class MockDB:
        snap_attributes = ['feelings', 'pose', 'color_image', 'depth_image']

        def __init__(self):
            self.users = {}
            self.snapshots = defaultdict(dict)

        def store_user(self, user_id, info):
            self.users[user_id] = info

        def store_parser_result(self, user_id, timestamp, parser_name,
                                parser_result):
            snapshots = self.snapshots[f'user_{user_id}']
            if timestamp not in snapshots:
                snapshots[timestamp] = {}
            snapshot[timestamp][parser_name] = parser_result

        def users(self):
            for user_id, info in self.users.__iter__():
                yield {'user_id': info['user_id'],
                       'username': info['username']}

        def get_user(self, user_id):
            user = self.users[user_id]
            return user['info']

        def snapshots(self, user_id):
            snapshots = self.snapshots[f'user_{user_id}']
            for timestamp, snapshot in snapshots.__iter__():
                yield {'snapshot_id': timestamp, 'datetime':
                    timestamp}

        def get_snapshot(self, user_id, snap_id):
            snap = self.snapshots[f'user_{user_id}'][snap_id]
            return {
                'snapshot_id': snap_id,
                'datetime': snap_id,
                'attributes': [attr for attr in MockDB.snap_attributes if
                               attr in snap]
            }

        def get_snapshot_attr(self, user_id, snap_id, attr):
            snap = self.snapshots[f'user_{user_id}'][snap_id]
            if attr in snap:
                return {attr: snap[attr]}
            return {attr: ''}

        def get_image(self, user_id, snap_id, image_type):
            snap = self.snapshots[f'user_{user_id}'][snap_id]
            if image_type in snap:
                return snap[image_type][0]
            return ''

    db = MockDB()
    db.store_user(user.user_id, MessageToJson(user))
    db.store_parser_result(user.user_id, snapshot.datetime, 'pose',
                           MessageToJson(snapshot.pose))
    return db


def serialize_to_file(rp, entity):
    serialized_entity = entity.SerializeToString()
    rp.write(struct.pack('I', len(serialized_entity)))
    rp.write(serialized_entity)
