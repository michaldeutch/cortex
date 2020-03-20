import requests
import logging

logger = logging.getLogger(__name__)


class Uploader:
    def __init__(self, host, port, serializer):
        self.url = f'http://{host}:{port}/'
        self.headers = {'Content-Type': serializer.content_type}
        self.serializer = serializer

    def __repr__(self):
        return f'Uploader to url={self.url}, serializer={self.serializer}'

    def upload(self, message):
        logger.debug(f'{self} posting a message')
        resp = requests.post(self.url, headers=self.headers,
                             data=self.serializer.serialize(message))
        return resp.ok
