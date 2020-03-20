"""
deserializers is meant to decouple the message format
in the mind file from the reader itself.
Meant to add more deserializers if the format changes.
"""


class ProtoDes:
    def __repr__(self):
        return 'ProtoDes'

    def deserialize(self, from_type, to_bytes):
        to_bytes.ParseFromString(from_type)
