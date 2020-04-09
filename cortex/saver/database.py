from urllib.parse import urlparse

from ..utils.impl_store import ImplementationStore

from pymongo import MongoClient


class Database:

    impl_store = ImplementationStore()

    def __init__(self, url):
        self.url = urlparse(url)
        self.impl = self.impl_store.get_impl(self.url.scheme)(url)

    def __enter__(self):
        return self.impl

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.impl.close()

    @impl_store.implementation('mongodb')
    class MongoDB:
        def __init__(self, url, client=None):
            self.client = client
            if client is None:
                self.client = MongoClient(url)
            self.db = self.client["thoughts"]

        def store_user(self, user_id, info):
            users = self.db["users"]
            users.insert_one({
                '_id': user_id,
                'info': info
            })

        def store_snapshot(self, user_id, timestamp, info):
            self.insert_snapshot(user_id, {
                '_id': f'{timestamp}.info',
                'info': info
            })

        def store_feelings(self, user_id, timestamp, feelings):
            self.insert_snapshot(user_id, {
                '_id': f'{timestamp}.feelings',
                'feelings': feelings
            })

        def store_pose(self, user_id, timestamp, pose):
            self.insert_snapshot(user_id, {
                '_id': f'{timestamp}.feelings',
                'pose': pose
            })

        def store_color_image(self, user_id, timestamp, color_image):
            self.insert_snapshot(user_id, {
                '_id': f'{timestamp}.color_image',
                'color_image': color_image
            })

        def store_depth_image(self, user_id, timestamp, depth_image):
            self.insert_snapshot(user_id, {
                '_id': f'{timestamp}.depth_image',
                'depth_image': depth_image
            })

        def users(self):
            users = self.db["users"]
            for user in users.find():
                yield user.info

        def insert_snapshot(self, user_id, document):
            snapshot = self.db[user_id]
            snapshot.insert_one(document)

        def close(self):
            self.client.close()