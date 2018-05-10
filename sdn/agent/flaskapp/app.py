import logging
from flask import Flask, request
from agent.sweep import PingSweep
from agent.logical_port import LogicalPort, CommandExecutor
from config.flask_config import get_config

app = Flask('Agent')
config = get_config()
debug_mode = config.getboolean('agent', 'debug')
logging.basicConfig(level=logging.DEBUG)


def __logical_port_from_data(data):
    return LogicalPort(net=data.get('net'),
                       net_ip=data.get('net_ip'),
                       router_ip=data.get('router_ip'),
                       local_ip=data.get('ip'))


@app.route('/ping/<path:target>', methods=['GET'])
def ping_target(target):
    sweeper = PingSweep()
    return str(sweeper.sweep(target=target))


@app.route('/create/logical_port', methods=['POST'])
def create_logical_port():
    data = request.get_json()
    logging.debug("Received %s", str(data))
    new_lp = __logical_port_from_data(data)
    new_lp.create(CommandExecutor())
    return 'Success\n'


@app.route('/remove/logical_port', methods=['POST'])
def create_logical_port():
    data = request.get_json()
    logging.debug("Received %s", str(data))
    new_lp = __logical_port_from_data(data)
    new_lp.delete(CommandExecutor())
    return 'Success\n'


app.run(config.get('agent', 'listen_address'),
        config.getint('agent', 'listen_port'),
        debug_mode)
