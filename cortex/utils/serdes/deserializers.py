from ..impl_store import ImplementationStore
from ..messages import cortex_pb2 as mind


class Deserializer:
    impl_store = ImplementationStore()

    @impl_store.implementation('proto')
    class ProtoDes:
        def deserialize_user(self, data):
            return self._deserialize(data, mind.User())

        def deserialize_snapshot(self, data):
            return self._deserialize(data, mind.Snapshot())

        @staticmethod
        def _deserialize(data, to):
            to.ParseFromString(data)
            return to

    def __init__(self, content_type):
        self.impl = self.impl_store.get_impl(content_type)()

    def deserialize_user(self, data):
        return self.impl.deserialize_user(data)

    def deserialize_snapshot(self, data):
        return self.impl.deserialize_snapshot(data)
