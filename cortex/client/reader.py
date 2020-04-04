import pathlib
import struct
import gzip
from ..utils.serdes.deserializers import Deserializer


class Reader:
    """
    Reads a gzipped mind file message by message
    assumes each message is prefixed by it's size
    """
    def __init__(self, mind_path, content_type):
        """
        :param mind_path: the path to the mind file, gzipped or not which is
                          built as sequence of messages, size and message
        :param deserializer:    turns each message into a type
        """
        self.rp = self._open_mind_file(mind_path)
        self.deserializer = Deserializer(content_type)
        self.user = self._parse_user()

    def __repr__(self):
        return f'Reader of mind file: {self.rp.name} , ' \
               f'parser: {self.deserializer}'

    def __iter__(self):
        while True:
            if self._is_end():
                self.rp.close()
                return
            snapshot = self._parse_snapshot()
            yield snapshot

    def _is_end(self):
        b = self.rp.read(1)
        self.rp.seek(-1, 1)
        return False if b else True

    def _get_next_message(self):
        message_len, = struct.unpack('I', self.rp.read(4))
        return self.rp.read(message_len)

    def _parse_user(self):
        message_bytes = self._get_message_bytes()
        return self.deserializer.deserialize_user(message_bytes)

    def _parse_snapshot(self):
        message_bytes = self._get_message_bytes()
        return self.deserializer.deserialize_snapshot(message_bytes)

    def _get_message_bytes(self):
        message_len, = struct.unpack('I', self.rp.read(4))
        return self.rp.read(message_len)

    @staticmethod
    def _open_mind_file(mind_path):
        if mind_path.endswith('.zip') or mind_path.endswith('.gz'):
            return gzip.GzipFile(mind_path, mode='rb')
        return pathlib.Path(mind_path).open('rb')
