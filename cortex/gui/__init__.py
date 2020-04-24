import json
import os
import subprocess

dirname, filename = os.path.split(os.path.abspath(__file__))
PACKAGE_FILE = f'{dirname}/app/package.json'


def update_proxy(url):
    json_file = open(PACKAGE_FILE, 'r')
    data = json.load(json_file)
    json_file.close()
    data['proxy'] = url
    json_file = open(PACKAGE_FILE, 'w+')
    json_file.write(json.dumps(data))
    json_file.close()


def run_server(host, port, api_host, api_port):
    update_proxy(f'http://{api_host}:{api_port}')
    os.environ['PORT'] = str(port)
    os.environ['HOST'] = str(host)
    print('starting server.. wait for about 60 seconds')
    subprocess.run([f'cd {dirname}/app && yarn start'],
                   shell=True, stdout=subprocess.DEVNULL)
