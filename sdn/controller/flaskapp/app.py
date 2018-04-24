import os, requests
from docker import DockerClient
from flask import Flask, request
from configparser import ConfigParser
from controller.controller import Controller
from controller.router import Router
from controller.network import Network
from controller.logical_port import LogicalPort


CONFIG_FILE = 'controller.conf'
CONFIG_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        CONFIG_FILE
    )
)


config = ConfigParser({'debug': 'True'})
config.read(CONFIG_PATH)

app = Flask('Controller')

controller = Controller(Router(str(config.get('docker', 'router_id')),
                               str(config.get('docker', 'router_endpoint')),
                               requests),
                        DockerClient(base_url=''))

@app.route('/')
@app.route('/index')
def get_index():
    return '<br/>'.join([
        '<b>Available endpoints:</b><br/>',
        '/create/network<br/>',
        '/create/logical_port<br/>'
    ])


@app.route('/create/network', methods=['POST'])
def create_network():
    data = request.get_json()
    new_network = Network(net_id=data.get('name'),
                          ip=data.get('cidr'))
    controller.add_network(new_network)
    return 'Success\n'


@app.route('/create/logical_port', methods=['POST'])
def create_logical_port():
    data = request.get_json()
    new_lp = LogicalPort(container=data.get('container'),
                         network=data.get('network'))
    controller.add_logical_port(new_lp)
    return 'Success\n'


app.run(str(config.get('main','listen_address')),
        config.getint('main', 'listen_port'),
        config.getboolean('main', 'debug'))