from flask import Blueprint, request
from flask import current_app as app
from auto_complete_api.services import ElasticSearch
import auto_complete_api.flask_utils as helpers

router = Blueprint('v0/messages', __name__)


@router.route('/', methods=['POST'])
@helpers.accepts('application/json')
def add():
    messages:list[str] = request.json
    service:ElasticSearch = app.config['services']['elasticsearch']
    service.add(messages)
    return 'OK'


@helpers.params(query=str)
def autocomplete_query(query):
    service:ElasticSearch = app.config['services']['elasticsearch']
    return service.autocomplete(query)


def autocomplete_choice():
    body = request.json
    return 'Not Implemented'


@router.route('/autocomplete', methods=['GET', 'POST'])
@helpers.json_serialize(headers={
    'Access-Control-Allow-Headers': 'content-type',
    'Access-Control-Allow-Methods': 'GET,POST,HEAD',
    'Access-Control-Allow-Origin': '*'
})
def autocomplete_router():
    if request.method == 'POST':
        return autocomplete_choice()

    return autocomplete_query()
