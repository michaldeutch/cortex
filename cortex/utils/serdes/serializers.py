import json

from ..impl_store import ImplementationStore
from google.protobuf.json_format import MessageToJson

"""
serializers is meant to decouple the message format
from the uploader.
Can add more serializers if the format changes.
"""


class Serializer:
    impl_store = ImplementationStore()

    @impl_store.implementation('proto')
    class ProtoSer:
        @staticmethod
        def serialize(message):
            return message.SerializeToString()

    @impl_store.implementation('proto2json')
    class Proto2JsonSer:
        @staticmethod
        def serialize(message):
            return json.loads(MessageToJson(message,
                                            preserving_proto_field_name=True,
                                            float_precision=20))

    @impl_store.implementation('json')
    class Json2BytesSer:
        @staticmethod
        def serialize(message):
            return json.dumps(message)

    def __init__(self, content_type):
        self.impl = self.impl_store.get_impl(content_type)()

    def serialize(self, message):
        return self.impl.serialize(message)
