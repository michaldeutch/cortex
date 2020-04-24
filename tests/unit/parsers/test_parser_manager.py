import json

import pytest
from google.protobuf.json_format import MessageToJson

from cortex.parsers import ParserManager


def test_find_parsers(manager):
    assert len(manager._parsers) >= 4


def test_run_parser(manager, snapshot):
    snap = json.loads(MessageToJson(snapshot,
                                    preserving_proto_field_name=True))
    data = {'snapshot': snap, 'user_id': 1}
    res = json.loads(manager.run_parser('pose', json.dumps(data)))
    assert res['user_id'] == 1
    assert json.loads(res['content']) == snap['pose']


@pytest.fixture
def manager():
    return ParserManager()