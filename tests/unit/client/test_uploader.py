import pytest

from cortex.utils.serdes.serializers import Serializer
from cortex.client.uploader import Uploader
from tests.conftest import USER_ID


def test_upload_success(web_server, uploader):
    assert uploader.upload_user(b'hey')


def test_upload_failure(uploader):
    with pytest.raises(Exception):
        uploader.upload_details(b'hey')


@pytest.fixture
def uploader(host, port):
    @Serializer.impl_store.implementation('text')
    class S:
        @staticmethod
        def serialize(message):
            return b'serialized-message'
    return Uploader(host, port, USER_ID, content_type='text')




