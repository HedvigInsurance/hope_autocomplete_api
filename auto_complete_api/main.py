from gevent import monkey; monkey.patch_all()

import os
import yaml
import logging
import werkzeug.exceptions

from flask import Flask
from gevent import pywsgi

import auto_complete_api.services as services
import auto_complete_api.endpoints as endpoints
import auto_complete_api.flask_utils as helpers


app = Flask('autocomplete_api')
logger = logging.getLogger('main')


@app.errorhandler(404)
@app.errorhandler(500)
@helpers.json_serialize()
def error_404(error:werkzeug.exceptions.HTTPException):
    return {
        'status': 'error',
        'payload': {'stats_code':error.code, 'message':error.description}
    }


def main():
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    logging.basicConfig(format='%(asctime)s :[%(levelname)s] %(name)s: %(message)s', level=logging.INFO)

    with open(ROOT_PATH+'/config.yaml', 'r') as f:
        config = yaml.load(f)

    # Instantiate services
    app.config['services'] = {
        'elasticsearch': services.ElasticSearch(**config['elasticsearch'])
    }

    # Register endpoints
    endpoints.register(app)

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
