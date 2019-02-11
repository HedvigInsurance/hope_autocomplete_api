import logging
from typing import Dict, List
from flask import current_app as app
from auto_complete_api.services import ElasticSearch

logger = logging.getLogger('api.messages')


def add(body: List[str]) -> None:
    service:ElasticSearch = app.config['services']['elasticsearch']
    service.add(body)


def autocomplete_get(query: str) -> Dict[str, float]:
    service:ElasticSearch = app.config['services']['elasticsearch']
    return service.autocomplete(query)


def autocomplete_post(body: str) -> None:
    service: ElasticSearch = app.config['services']['elasticsearch']
    submitted_message = body['submitted_response']['text']
    service.add([submitted_message])
    logger.info('User action: {}'.format(body))
