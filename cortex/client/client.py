import logging
from .uploader import Uploader
from .reader import Reader

logger = logging.getLogger(__name__)


# TODO - add integration test
def upload_sample(host, port, path):
    try:
        reader = Reader(path, content_type='proto')
        user = reader.user
        uploader = Uploader(host, port, user.user_id, content_type='proto')
        uploader.upload_user(user)
        for snapshot in reader:
            uploader.upload_snapshot(snapshot)
    except FileNotFoundError:  # TODO - not sure if this is enough,
        # maybe log the error
        print(f'Could not find {path}, upload failed')
    except ConnectionError:
        print(f'failed to connect with {host}:{port}')
    except Exception as err:
        print(f'Failed to read {path} and upload to {host}:{port}, err={err}')
