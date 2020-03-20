import pytest
from cortex.client.uploader import Uploader


def test_upload_success(web_server, uploader):
    assert uploader.upload(b'hey')


def test_upload_failure(uploader):
    with pytest.raises(Exception):
        uploader.upload(b'hey')


@pytest.fixture
def uploader(serializer, host, port):
    return Uploader(host, port, serializer)


@pytest.fixture
def serializer():
    class S:
        def __init__(self):
            self.content_type = 'text/enriched'

        def serialize(self, entity):
            return b'serialized-message'

    return S()
