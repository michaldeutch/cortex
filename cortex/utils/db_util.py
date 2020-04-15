from urllib.parse import urlparse

from bson.objectid import ObjectId

from cortex.utils.impl_util import ImplementationStore

from pymongo import MongoClient


class Database:
    snap_attributes = ['feelings', 'pose', 'color_image', 'depth_image']
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

        def store_parser_result(self, user_id, timestamp, parser_name,
                                parser_result):
            snapshots = self.db[f'user_{user_id}']
            snapshots.update_one({'timestamp': timestamp},
                                 {'$push': {parser_name: parser_result}},
                                 upsert=True)

        def users(self):
            users = self.db['users']
            for user in users.find():
                info = user['info']
                yield {'user_id': info['user_id'],
                       'username': info['username']}

        def get_user(self, user_id):
            users = self.db['users']
            user = users.find_one({'_id': user_id})
            return user['info']

        def snapshots(self, user_id):
            user_snapshots = self.db[f'user_{user_id}']
            for snapshot in user_snapshots.find():
                yield {'snapshot_id': str(snapshot['_id']), 'datetime':
                    snapshot['timestamp']}

        def get_snapshot(self, user_id, snap_id):
            snap = self._get_snapshot(user_id, snap_id)
            return {
                'snapshot_id': str(snap['_id']),
                'datetime': snap['timestamp'],
                'attributes': [attr for attr in Database.snap_attributes if
                               attr in snap]
            }

        def get_snapshot_attr(self, user_id, snap_id, attr):
            snap = self._get_snapshot(user_id, snap_id)
            if attr in snap:
                return {attr: snap[attr]}
            return {attr: ''}

        def get_image(self, user_id, snap_id, image_type):
            snap = self._get_snapshot(user_id, snap_id)
            if image_type in snap:
                return snap[image_type][0]
            return ''

        def _get_snapshot(self, user_id, snap_id):
            snapshots = self.db[f'user_{user_id}']
            if isinstance(snap_id, str):
                snap_id = ObjectId(snap_id)
            return snapshots.find_one({'_id': snap_id})

        def close(self):
            self.client.close()