import json

import pytest

from cortex.utils.serdes.serializers import Serializer
from cortex.server.publish_manager import PublishManager
from tests.conftest import USER_ID

_published = []
_CONTENT_TYPE = 'proto'
_serializer = Serializer(_CONTENT_TYPE)


def test_publish_user(publisher, user):
    publisher.publish_user(USER_ID, _serializer.serialize(user), _CONTENT_TYPE)
    assert len(_published) == 1


def test_publish_snapshot(publisher, snapshot):
    publisher.publish_snapshot(USER_ID, _serializer.serialize(snapshot),
                               _CONTENT_TYPE)
    assert len(_published) == 1


def test_save_snapshot_image(publisher):
    data = 'Y29sb3JfZGF0YQ=='
    snapshot = {'color_image': {
        'width': 5,
        'height': 7,
        'data': 'Y29sb3JfZGF0YQ=='
    }}
    publisher._save_snapshot_images(snapshot)
    path = snapshot['color_image']['path']
    with open(path, 'r') as content_file:
        assert json.loads(content_file.read()) == data


def test_prepare_user(publisher, user):
    serialized_user = json.loads(publisher._prepare_message(USER_ID, user, _CONTENT_TYPE))
    assert serialized_user['user_id'] == str(USER_ID)
    assert serialized_user['user']['user_id'] == str(USER_ID)


def test_prepare_snapshot(publisher, snapshot):
    serialized_snap = json.loads(publisher._prepare_message(USER_ID, snapshot,
                                                 _CONTENT_TYPE,
                                                 is_snapshot=True))
    assert serialized_snap['user_id'] == str(USER_ID)
    assert serialized_snap['snapshot']


@pytest.fixture
def publisher():
    def publish(message):
        _published.append(message)

    with PublishManager(publish) as publisher:
        yield publisher
        _published.clear()
