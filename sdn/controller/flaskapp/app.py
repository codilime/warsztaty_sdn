import logging
import requests
import traceback
from docker import DockerClient
from flask import Flask, request, jsonify
from sdn.controller.controller import Controller
from sdn.controller.router import Router
from sdn.controller.network import Network
from sdn.controller.logical_port import LogicalPort
from sdn.controller.container import Container
from sdn.config.flask_config import get_config


app = Flask('Controller')
config = get_config()
debug_mode = config.getboolean('controller', 'debug')
logging.basicConfig(level=logging.DEBUG)

controller = Controller(Router(id=config.get('router', 'docker_id'),
                               ip='http://%s:%s' % (config.get('router', 'docker_ip'),
                                                    config.get('router', 'listen_port')),
                               poster=requests),
                        DockerClient(base_url=config.get('docker', 'docker_socket')))


class ServerError(Exception):

    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message, self.status_code, self.payload = message, status_code, payload

    def to_dict(self):
        return {'message': self.message, 'payload': self.payload or {}}


@app.errorhandler(ServerError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def _assert_proper_request(req):
    if (req.content_type != 'application/json' or not hasattr(req, 'json')):
        raise ServerError(message='Malformed request, expected json payload and type',
                         status_code=400)


@app.route('/hello', methods=['GET'])
def hello():
    return str('hello')


@app.route('/')
@app.route('/index')
def get_index():
    return '<br/><br/>'.join([
        '<b>Available endpoints:</b>',
        '<ul><li>/create/network <br>POST - {"name": "xyz", "cidr": "10.20.0.0/16"}</li>',
        '<li>/create/logical_port <br>POST - {"container_name": "dock", "network_name": "xyz"}</li>',
        '</ul>'
    ])


@app.route('/force_clean', methods=['POST'])
def force_clean():
    controller.clean()
    return 'Success\n'


@app.route('/create/network', methods=['POST'])
def create_network():
    _assert_proper_request(request)

    try:
        data = request.get_json()
        new_network = Network(net_id=data['name'],
                              ip=data['cidr'])
        controller.add_network(new_network)
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating network',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/create/container', methods=['POST'])
def create_container():
    _assert_proper_request(request)

    try:
        data = request.get_json()
        controller.add_container(id=data['id'])
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating network',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/delete/container', methods=['POST'])
def delete_container():
    _assert_proper_request(request)

    try:
        data = request.get_json()
        container = Container(id=data['id'], ip='', poster=None, docker_client=controller.docker_client) #FIXME this should be looked up in an in-memory db
        container.stop()
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating network',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/create/logical_port', methods=['POST'])
def create_logical_port():
    _assert_proper_request(request)

    try:
        data = request.get_json()
        raw_container = data.get('container')
        container = Container(id=raw_container['id'],
                              ip=raw_container['ip'],
                              poster=requests,
                              docker_client=controller.docker_client)
        network = controller.get_network(data.get('net_id'))
        new_lp = LogicalPort(container=container, network=network)
        controller.add_logical_port(new_lp)
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating logical port',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


if __name__ == '__main__':
    app.run(config.get('controller', 'listen_address'),
            config.getint('controller', 'listen_port'),
            debug_mode)