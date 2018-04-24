import logging
from flask import Flask, request
from agent.sweep import PingSweep
from agent.logical_port import LogicalPort, CommandExecutor
from config.flask_config import get_config


app = Flask('Agent')
config = get_config()
debug_mode = config.getboolean('agent', 'debug')
logging.basicConfig(level=logging.DEBUG)

@app.route('/ping/<target>', methods=['GET'])
def ping_target(target):
    sweeper = PingSweep()
    return str(sweeper.sweep(target=target))


@app.route('/create/logical_port', methods=['POST'])
def create_logical_port():
    data = request.get_json()
    new_lp = LogicalPort(net=data.get('net'),
                         local_ip=data.get('ip'))
    new_lp.create(CommandExecutor())
    return 'Success\n'

app.run(config.get('agent','listen_address'),
        config.getint('agent', 'listen_port'),
        debug_mode)