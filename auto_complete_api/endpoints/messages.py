import logging
from typing import Dict, List
from flask import current_app as app
from auto_complete_api.services import ELASTICSEARCH, USERACTIONLOG
from auto_complete_api.services import ElasticSearchService, UserActionLogService

logger = logging.getLogger('api.messages')


def add(body: List[str]) -> None:
    service:ElasticSearchService = app.config['services'][ELASTICSEARCH]
    service.add(body)


def autocomplete_get(query: str) -> Dict[str, float]:
    service:ElasticSearchService = app.config['services'][ELASTICSEARCH]
    return service.autocomplete(query)


def autocomplete_post(body: str) -> None:
    es: ElasticSearchService = app.config['services'][ELASTICSEARCH]
    action_log: UserActionLogService = app.config['services'][USERACTIONLOG]

    submitted_message = body['submitted_response']['text']

    es.add([submitted_message])
    action_log.persist(**body)

