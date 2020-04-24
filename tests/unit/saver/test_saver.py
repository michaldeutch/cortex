import json

from cortex.saver import Saver


def test_save(db):
    saver = Saver('', db)
    saver.save('pose', json.dumps({
        'user_id': 1,
        'timestamp': 132,
        'content': 'data'
    }))
    assert db.db.get_snapshot(1, 132) is not None
