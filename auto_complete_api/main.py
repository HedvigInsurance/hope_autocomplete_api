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
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    with open(ROOT_PATH+'/config.yaml', 'r') as f:
        config = yaml.load(f)

    # Instantiate services
    app.config['services'] = {
        'elasticsearch': services.ElasticSearch(**config['elasticsearch'])
    }

    # Register endpoints
    endpoints.register(app)

    # Run server
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()


if __name__ == '__main__':
    main()
