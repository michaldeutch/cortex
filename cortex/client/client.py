import logging
from .uploader import Uploader
from .reader import Reader
from google.protobuf.json_format import MessageToJson

from ..utils.messages.cortex_pb2 import Feelings, Pose, ColorImage, DepthImage

logger = logging.getLogger(__name__)


def upload_sample(host, port, path):
    try:
        reader = Reader(path, content_type='proto')
        user = reader.user
        uploader = Uploader(host, port, user.user_id, content_type='proto')
        uploader.upload_user(user)
        logger.debug(f'Uploaded user message for userId={user.user_id}')
        for snapshot in reader:
            uploader.upload_snapshot(snapshot)
            logger.debug(f'Uploaded snapshot message for userId'
                         f'={user.user_id}')
    except FileNotFoundError:
        print(f'Could not find {path}, upload failed')
    except ConnectionError:
        print(f'failed to connect with {host}:{port}')
    except Exception as err:
        print(f'Failed to read {path} and upload to {host}:{port}, err={err}')
