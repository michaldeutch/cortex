from urllib.parse import urlparse

from ..utils.impl_store import ImplementationStore

import pymongo

class Database:

    impl_store = ImplementationStore()

    def __init__(self, url):
        self.url = urlparse(url)
        self.impl = self.impl_store.get_impl(self.url.scheme)(self.url)

    def __enter__(self):
        return self.impl

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.impl.close()

    @impl_store.implementation('mongodb')
    class MongoDB:
        def __init__(self, url):
            pass

        def close(self):
            pass