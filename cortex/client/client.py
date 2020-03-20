import logging
from .uploader import Uploader
from .reader import Reader
from .deserializers import ProtoDes
from .serializers import ProtoSer

logger = logging.getLogger(__name__)


# TODO - add integration test
def upload_sample(host, port, path):
    try:
        reader = Reader(path, ProtoDes())
        uploader = Uploader(host, port, ProtoSer())

        uploader.upload(reader.user)
        for snapshot in reader:
            uploader.upload(snapshot)
    except FileNotFoundError:  # TODO - not sure if this is enough,
        # maybe log the error
        print(f'Could not find {path}, upload failed')
    except ConnectionError:
        print(f'failed to connect with {host}:{port}')
    except Exception:
        print(f'Failed to read {path} and upload to {host}:{port}')
