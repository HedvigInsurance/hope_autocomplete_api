from gevent import monkey; monkey.patch_all()

import os
import yaml
import json
import logging
import werkzeug.exceptions

from flask import Flask
from gevent import pywsgi

import auto_complete_api.services as services
import auto_complete_api.endpoints as endpoints


app = Flask('autocomplete_api')
logger = logging.getLogger('main')


@app.errorhandler(werkzeug.exceptions.HTTPException)
def http_errorhandler(error:werkzeug.exceptions.HTTPException):
    return (
        json.dumps({
            'status': 'error',
            'payload': {
                'status_code':error.code,
                'message':error.description
            }
        }).encode('utf-8'),
        error.code,
        {'Content-Type': 'application/json; charset=utf-8'}
    )


def configure(config_file:str):
    logging.basicConfig(format='%(asctime)s :[%(levelname)s] %(name)s: %(message)s', level=logging.INFO)

    with open(config_file, 'r') as f:
        config = yaml.load(os.path.expandvars(f.read()))

    # Instantiate services
    app.config['services'] = {
        'elasticsearch': services.ElasticSearch(**config['elasticsearch'])
    }

    # Register endpoints
    endpoints.register(app)

    return config


def main():
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    configure(ROOT_PATH+'/config.yaml')

    # Run server
    try:
        logger.info('Service starting')

        app.config['services']['elasticsearch'].wait_for_cluster(30)
        app.config['services']['elasticsearch'].create_index()

        logger.info('Service started')

        server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Caught CTRL+C')
    logging.info('Service stopped')


if __name__ == '__main__':
    main()
