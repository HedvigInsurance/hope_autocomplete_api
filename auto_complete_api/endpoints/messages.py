import logging
from typing import Dict, List
from flask import current_app as app
from auto_complete_api.services import ElasticSearch

logger = logging.getLogger('api.messages')


def add(messages: List[str]) -> None:
    service:ElasticSearch = app.config['services']['elasticsearch']
    service.add(messages)


def autocomplete_get(query: str) -> Dict[str, float]:
    service:ElasticSearch = app.config['services']['elasticsearch']
    return service.autocomplete(query)


def autocomplete_post(action: str) -> None:
    logger.info('User action: {}'.format(action))
