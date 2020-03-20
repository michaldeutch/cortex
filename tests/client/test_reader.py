import pytest


def test_user(reader, user):
    assert reader.user == user


def test_snapshot(reader, snapshot):
    for snap in reader:
        assert snap == snapshot
        break
    else:
        pytest.fail('expecting one snapshot, none received')
