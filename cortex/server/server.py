from concurrent.futures import ThreadPoolExecutor

from flask import Flask
from flask import request

from cortex.server.publish_manager import PublishManager

app = Flask(__name__)
NUM_THREADS = 5


def run_server(host, port, publish):
    executor = ThreadPoolExecutor(NUM_THREADS)
    with PublishManager(publish) as publisher_manager:
        @app.route('/user/<user_id>', methods=['POST'])
        def handle_user(user_id):
            executor.submit(publisher_manager.publish_user, user_id,
                            request.data, request.content_type)
            return 'OK'

        @app.route('/snapshot/<user_id>', methods=['POST'])
        def handle_snapshot(user_id):
            executor.submit(publisher_manager.publish_snapshot, user_id,
                            request.data, request.content_type)
            return 'OK'

        app.run(host, port)
        executor.shutdown()
