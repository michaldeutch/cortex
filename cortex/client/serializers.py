"""
serializers is meant to decouple the message format
from the uploader.
Can add more serializers if the format changes.
"""


class ProtoSer:
    def __init__(self):
        self.content_type = 'application/protobuf'

    def __repr__(self):
        return 'ProtoSer'

    def serialize(self, from_bytes):
        return from_bytes.SerializeToString()
