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
def hello():
    return str('hello')


@app.route('/create/network', methods=['POST'])
def create_network():
    data = request.get_json()
    router.add_network(name=data['id'])
    return 'Success\n'


@app.route('/create/logical_port', methods=['POST'])
def create_logical_port():
    data = request.get_json()
    router.add_logical_port(net=data['net_id'],
                            ip=data['ip'])
    return 'Success\n'


if __name__ == '__main__':
    app.run(config.get('router','listen_address'),
            config.getint('router', 'listen_port'),
            debug_mode)