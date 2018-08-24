import logging
from flask import Flask, request
from sdn.router.router import Router, CommandExecutor
from sdn.router.interface_finder import InterfaceFinder
from sdn.config.flask_config import get_config

app = Flask('Router')
config = get_config()
debug_mode = config.getboolean('router', 'debug')
logging.basicConfig(level=logging.DEBUG)

router = Router(CommandExecutor, InterfaceFinder)


@app.route('/hello', methods=['GET'])
def hello() -> str:
    return str('hello')


@app.route('/create/network', methods=['POST'])
def create_network() -> str:
    data = request.get_json()
    router.add_network(name=data['name'])
    return 'Success\n'


@app.route('/network/<name>', methods=['DELETE'])
def delete_network(name) -> str:
    router.remove_network(name=name)
    return 'Success\n'


@app.route('/create/logical_port', methods=['POST'])
def create_logical_port() -> str:
    data = request.get_json()
    router.add_logical_port(net=data['name'],
                            ip=data['ip'])
    return 'Success\n'


@app.route('/logical_port', methods=['DELETE'])
def delete_logical_port() -> str:
    data = request.get_json()
    router.remove_logical_port(net=data['name'],
                            ip=data['ip'])
    return 'Success\n'


@app.route('/help', methods=['GET'])
def list_routes():
    return '\n'.join(['%s' % rule for rule in app.url_map.iter_rules()])


if __name__ == '__main__':
    app.run(config.get('router', 'listen_address'),
            config.getint('router', 'listen_port'),
            debug_mode)
