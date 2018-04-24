import traceback
from flask import Flask, request
from agent.sweep import PingSweep
from config.flask_config import get_config


app = Flask('Agent')
config = get_config()
debug_mode = config.getboolean('agent', 'debug')


@app.route('/ping/<target>', methods=['GET'])
def ping_target(target):
    sweeper = PingSweep()
    return str(sweeper.sweep(target=target))


app.run(config.get('agent','listen_address'),
        config.getint('agent', 'listen_port'),
        debug_mode)