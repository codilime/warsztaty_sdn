import logging
import traceback
from typing import Dict, Optional

import requests
import json
from docker import DockerClient
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask.wrappers import Response, Request
from flask.json import JSONEncoder
from sdn.config.flask_config import get_config
from sdn.controller.controller import Controller
from sdn.controller.logical_port import LogicalPort
from sdn.controller.network import Network
from sdn.controller.router import Router
from sdn.controller.container import Container

app = Flask('Controller')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
config = get_config()
debug_mode = config.getboolean('controller', 'debug')
logging.basicConfig(level=logging.DEBUG)

controller = Controller(Router(id=config.get('router', 'docker_id'),
                               ip='http://%s:%s' % (config.get('router', 'docker_ip'),
                                                    config.get('router', 'listen_port')),
                               poster=requests),
                        DockerClient(base_url=config.get('docker', 'docker_socket')),
                        poster=requests)


class ServerError(Exception):

    def __init__(self, message: str, status_code: int, payload: Optional[str] = None) -> None:
        Exception.__init__(self)
        self.message, self.status_code, self.payload = message, status_code, payload

    def to_dict(self) -> Dict[str, str]:
        return {'message': self.message, 'payload': self.payload or {}}


class DictJsonEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Container):
            return {"id": o.id}
        elif isinstance(o, Network):
            return o.__dict__
        elif isinstance(o, LogicalPort):
            return {
                "net_id": o.network.id,
                "container": {
                     "id": o.container.id
                }
            }
        return super(DictJsonEncoder, self).default(o)

@app.errorhandler(ServerError)
def handle_invalid_usage(error: ServerError) -> Response:
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def _assert_proper_request(req: Request) -> None:
    if req.content_type != 'application/json' or not hasattr(req, 'json'):
        raise ServerError(message='Malformed request, expected json payload and type',
                          status_code=400)


@app.route('/hello', methods=['GET'])
def hello() -> str:
    return str('hello')


@app.route('/')
@app.route('/index')
def get_index() -> str:
    return '<br/><br/>'.join([
        '<b>Available endpoints:</b>',
        '<ul><li>/create/network <br>POST - {"name": "xyz", "cidr": "10.20.0.0/16"}</li>',
        '<li>/create/logical_port <br>POST - {"container_name": "dock", "network_name": "xyz"}</li>',
        '</ul>'
    ])


@app.route('/force_clean', methods=['POST'])
def force_clean() -> str:
    controller.clean()
    return 'Success\n'

@app.route('/network', methods=['POST'])
@app.route('/create/network', methods=['POST'])
def create_network() -> str:
    _assert_proper_request(request)

    try:
        data = request.get_json()
        new_network = Network(net_id=data['id'],
                              ip=data['ip'])
        controller.add_network(new_network)
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating network',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/networks', methods=['GET'])
def list_networks() -> str:
    try:
        return json.dumps(controller.list_networks(), cls=DictJsonEncoder)
    except:
        raise ServerError(message='Internal server error when listing networks',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/container', methods=['POST'])
@app.route('/create/container', methods=['POST'])
def create_container() -> str:
    _assert_proper_request(request)

    try:
        data = request.get_json()
        controller.add_container(id=data['id'], code_path=config.get('agent', 'sdn_path'))
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating container',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')

@app.route('/container/<id>', methods=['DELETE'])
def delete_container_id(id) -> str:
    try:
        controller.remove_container(id=id)
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error deleting a container',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')

@app.route('/delete/container', methods=['POST'])
def delete_container() -> str:
    _assert_proper_request(request)

    try:
        data = request.get_json()
        controller.remove_container(id=data['id'])
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error deleting a container',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/containers', methods=['GET'])
def list_containers() -> str:
    try:
        return json.dumps(controller.list_containers(), cls=DictJsonEncoder)
    except:
        raise ServerError(message='Internal server error when listing containers',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/logical_port', methods=['POST'])
@app.route('/create/logical_port', methods=['POST'])
def create_logical_port() -> str:
    _assert_proper_request(request)

    try:
        data = request.get_json()
        raw_container = data.get('container')
        container = controller.get_container(raw_container['id'])
        network = controller.get_network(data.get('net_id'))
        new_lp = LogicalPort(container=container, network=network)
        controller.add_logical_port(new_lp)
        return 'Success\n'
    except:
        raise ServerError(message='Internal server error creating logical port',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')


@app.route('/logical_ports', methods=['GET'])
def list_logical_ports() -> str:
    try:
        return json.dumps(controller.list_logical_ports(), cls=DictJsonEncoder)
    except:
        raise ServerError(message='Internal server error when listing logical_ports',
                          status_code=500,
                          payload=traceback.format_exc() if debug_mode else '')

@app.route('/help', methods=['GET'])
def list_routes():
    return '\n'.join(['%s' % rule for rule in app.url_map.iter_rules()])


if __name__ == '__main__':
    app.run(config.get('controller', 'listen_address'),
            config.getint('controller', 'listen_port'),
            debug_mode)
