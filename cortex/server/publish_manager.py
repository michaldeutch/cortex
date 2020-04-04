import json
import tempfile
import os
import logging
import shutil

from ..utils.serdes.deserializers import Deserializer
from ..utils.serdes.serializers import Serializer

logger = logging.getLogger(__name__)


class PublishManager:
    def __init__(self, publish_method):
        self.temp_dir = tempfile.mkdtemp()
        self.publish_method = publish_method

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        shutil.rmtree(self.temp_dir)

    def __repr__(self):
        return f'PublishManager with publisher={self.publish_method}, ' \
               f'saves images to {self.temp_dir}'

    def publish_user(self, user_id, data, content_type):
        user = Deserializer(content_type).deserialize_user(data)
        message = self._prepare_message(user_id, user, content_type)
        self.publish_method(message)

    def publish_snapshot(self, user_id, data, content_type):
        snapshot = Deserializer(content_type).deserialize_snapshot(data)
        message = self._prepare_message(user_id, snapshot, content_type,
                                        is_snapshot=True)
        self.publish_method(message)

    def _prepare_message(self, user_id, content, content_type,
                         is_snapshot=False):
        to_json_serializer = Serializer(f'{content_type}2json')
        serialized_content = to_json_serializer.serialize(content)
        message = 'user'
        if is_snapshot:
            message = 'snapshot'
            self._save_snapshot_images(serialized_content)
        ret = {
            'userId': str(user_id),  # longs are strings
            message: serialized_content
        }
        return Serializer('json').serialize(ret)

    def _save_snapshot_images(self, snapshot):
        def save_image(image_name):
            try:
                image = snapshot[image_name]
                width = image['width']
                height = image['height']
                fd, path = tempfile.mkstemp(suffix=f'{width}x{height}',
                                            dir=self.temp_dir)
                self._save_data(image['data'], fd)
                snapshot[image_name] = path
            except Exception as err:
                logger.error(f'failed to save {image_name},'
                             f' {err}')
        save_image('colorImage')
        save_image('depthImage')

    @staticmethod
    def _save_data(data, fd):  # TODO - save image in a better format
        with os.fdopen(fd, 'w') as tmp:
            tmp.write(json.dumps(data))
