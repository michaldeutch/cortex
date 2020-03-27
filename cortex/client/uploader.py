import requests
import logging
from cortex.serdes.serializers import Serializer


logger = logging.getLogger(__name__)


class Uploader:
    def __init__(self, host, port, user_id, content_type, num_trials=10):
        self.url = f'http://{host}:{port}'
        self.headers = {'Content-Type': content_type}
        self.serializer = Serializer(content_type)
        self.user_id = user_id
        self.num_trials = num_trials

    def __repr__(self):
        return f'Uploader to url={self.url}, serializer={self.serializer}, ' \
               f'user_id={self.user_id}'

    def upload_user(self, message):
        return self._upload(message, 'user')

    def upload_snapshot(self, message):
        return self._upload(message, 'snapshot')

    def _upload(self, message, message_type):
        logger.debug(f'{self} posting a message')
        t = 0
        while t < self.num_trials:
            resp = requests.post(f'{self.url}/{message_type}/{self.user_id}',
                                 headers=self.headers,
                                 data=self.serializer.serialize(message))
            if resp.ok:
                return True  # For testing
            t += 1
        raise ConnectionError(f'Attempted to upload message '
                              f'{self.num_trials} times, and failed')
