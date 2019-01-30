from operator import itemgetter

import nltk
import emoji
import elasticsearch
from elasticsearch_dsl import Search


def sentence_split(text:str):
    re = emoji.get_emoji_regexp()

    return list(
        filter(
            lambda x: re.match(x) is None,
            sum(
                list(map(nltk.sent_tokenize, re.split(text))),
                []
            )
        )
    )


class ElasticSearch(object):
    def __init__(self, hosts, index):
        self._index = index
        self._client = elasticsearch.Elasticsearch(hosts=hosts)

    def autocomplete(self, query):
        def fix_query(query: str):
            query = query.strip().lower()

            if query[0] == '"':
                query = query[1:]
            if query[-1] == '"':
                query = query[:-1]

            return query

        def score_tune(query: str, score: float, text: str):
            score /= max(1, len(text) - len(query))
            if text.lower().startswith(query):
                score *= 10

            return {'score': score, 'text': text.strip()}

        query = fix_query(query)

        result = list(map(
            lambda x: {'score': x.meta.score, 'text': x.text},
            Search(using=self._client, index=self._index).query('match_phrase_prefix', text=query).execute().hits
        ))

        if len(result) == 0:
            result = map(
                lambda x: {'score': x.meta.score, 'text': x.text},
                Search(using=self._client, index=self._index).query('match', text=query).execute().hits
            )

        return sorted(
            map(
                lambda x: score_tune(query, **x),
                result
            ),
            key=itemgetter('score'),
            reverse=True
        )

    def add(self, docs):
        pass
