import json

from flask import Flask
from flask import jsonify
from flask import send_file
from flask import request

from datetime import datetime

app = Flask(__name__)
NOT_FOUND = 'None'


def run_api_server(host, port, db):
    @app.route('/users', methods=['GET'])
    def get_users():
        return jsonify([user for user in db.users()])

    @app.route('/users/<user_id>', methods=['GET'])
    def get_user(user_id):
        user = db.get_user(user_id)
        if 'birthday' in user:
            user['birthday'] = datetime.fromtimestamp(user['birthday'] /
                                                      1000).date()
        return jsonify(user)

    @app.route('/users/<user_id>/snapshots', methods=['GET'])
    def get_snapshots(user_id):
        snapshots = []
        for snap in db.snashots(user_id):
            if 'datetime' in snap:
                snap['datetime'] = datetime.fromtimestamp(snap['datetime'])
                snapshots.append(snap)
        return jsonify(snapshots)

    @app.route('/users/<user_id>/snapshots/<snapshot_id>', methods=['GET'])
    def get_snapshot(user_id, snapshot_id):
        return jsonify(db.get_snapshot(user_id, snapshot_id))

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<attr>',
               methods=['GET'])
    def get_attr(user_id, snapshot_id, attr):
        if attr.endswith('image'):
            return {'data_url': f'{request.url}/data'}
        res = db.get_snapshot_attr(user_id, snapshot_id, attr)
        if not res[attr]:
            return NOT_FOUND
        return res

    @app.route('/users/<user_id>/snapshots/<snapshot_id>/<image_type'
               '>/data',
               methods=['GET'])
    def get_data(user_id, snapshot_id, image_type):
        if image_type != 'color_image' and image_type != 'depth_image':
            return NOT_FOUND
        image = json.loads(db.get_image(user_id, snapshot_id, image_type))
        return send_file(image)

    app.run(host, port)
