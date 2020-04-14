import json
import sys
import logging

import click
import requests

logger = logging.getLogger(__name__)

help = 'Access API server on this'

def cortex(command):
    host_option = click.option('-h', '--host', type=str, help=f'{help} host',
                               default='127.0.0.1')
    port_option = click.option('-p', '--port', type=int, help=f'{help} port',
                               default=5000)
    return click.command()(host_option(port_option(command)))

@cortex
@click.argument('user_id', type=int)
def get_users(host, port):
    url = f'http://{host}:{port}/users'
    resp = requests.get(url)
    if resp.ok:
        users = json.loads(resp.content.decode('utf-8'))
        for user in users:
            print(user)
    else:
        print_error_response(url)

@cortex
@click.argument('user_id', type=int)
def get_user(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}'
    resp = requests.get(url)
    if resp.ok:
        print(json.loads(resp.content.decode('utf-8')))
    else:
        print_error_response(url)


@cortex
@click.argument('user_id', type=int)
def get_snapshots(host, port, user_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots'
    resp = requests.get(url)
    if resp.ok:
        snapshots = json.loads(resp.content.decode('utf-8'))
        for snap in snapshots:
            print(snap)
    else:
        print_error_response(url)

@cortex
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=str)
def get_snapshot(host, port, user_id, snapshot_id):
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}'
    resp = requests.get(url)
    if resp.ok:
        print(json.loads(resp.content.decode('utf-8')))
    else:
        print_error_response(url)

@cortex
@click.argument('user_id', type=int)
@click.argument('snapshot_id', type=str)
@click.argument('parser', type=str)
@click.option('-s', '--save', type=str, help=f'saving result in a file',
              default='')
def get_snapshot(host, port, user_id, snapshot_id, parser, save):
    url = f'http://{host}:{port}/users/{user_id}/snapshots/{snapshot_id}/' \
          f'{parser}'
    resp = requests.get(url)
    if resp.ok:
        res = json.loads(resp.content.decode('utf-8'))
        if save:
            with open(save, 'w') as file:
                file.write(res)
        else:
            print(res)
    else:
        print_error_response(url)

def print_error_response(url):
    print(f'sorry, failed to get response from {url}. Try again!')

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'get-users':
            get_users(sys.argv[2:])
        elif sys.argv[1] == 'get-user':
            get_user(sys.argv[2:])
        elif sys.argv[1] == 'get-snapshots':
            get_snapshots(sys.argv[2:])
        else:
            print('TRY: python -m cortex.parsers parse/run-parser --help')
    except Exception as error:
        logger.error('parsers main failed', error)
        print(f'An error occurred while running parser, {error}')
        sys.exit(1)
