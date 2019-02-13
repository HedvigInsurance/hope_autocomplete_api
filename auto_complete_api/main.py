from gevent import monkey; monkey.patch_all()

import os
import yaml
import logging

import connexion
from gevent import pywsgi

import auto_complete_api.services as services


SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger('main')
cnx_app = connexion.FlaskApp('autocomplete_api')


def configure(config_file:str):
    logging.basicConfig(
        format='%(asctime)s :[%(levelname)s] %(name)s: %(message)s',
        level=logging.INFO
    )

    with open(config_file, 'r') as f:
        config = yaml.load(os.path.expandvars(f.read()))

    # Instantiate services
    flask = cnx_app.app
    flask.config['services'] = {
        services.ELASTICSEARCH: services.ElasticSearchService(**config['elasticsearch']),
        services.USERACTIONLOG: services.UserActionLogService(**config['postgres'])
    }

    # Register endpoints
    cnx_app.add_api(SCRIPT_PATH+'/api_spec.yaml')

    return config


def main():
    configure(SCRIPT_PATH + '/config.yaml')

    # Run server
    logger.info('Service starting')
    try:
        cnx_app.app.config['services'][services.ELASTICSEARCH].wait_for_cluster(30)
        cnx_app.app.config['services'][services.ELASTICSEARCH].create_index()

        logger.info('Service started')

        server = pywsgi.WSGIServer(('0.0.0.0', 5000), cnx_app.app)
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('Caught CTRL+C')
    logging.info('Service stopped')


if __name__ == '__main__':
    main()
