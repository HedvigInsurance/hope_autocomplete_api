from operator import itemgetter

import time
import hashlib
import nltk
import emoji
import logging
import elasticsearch
from elasticsearch_dsl import Search


logger = logging.getLogger('es-service')


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
        logger.info('Using the following hosts: {}'.format(', '.join(hosts)))

    def wait_for_cluster(self, timeout=10):
        level = logging.getLogger('elasticsearch').level
        logging.getLogger('elasticsearch').setLevel(logging.ERROR)

        try:
            logger.info('Checking cluster availability')

            start_time = time.time()
            while (time.time()-start_time) < timeout:
                if self._client.ping():
                    logger.info('Cluster is up!')
                    return

                logger.info('Cluster is not yet up')
                time.sleep(1)

            raise TimeoutError('ES cluster is not available!')
        finally:
            logging.getLogger('elasticsearch').setLevel(level)

    def create_index(self):
        es = self._client
        index = self._index

        if es.indices.exists(index):
            logger.info('Index {} exists'.format(index))
            return

        logger.info('Attempting to create index {}'.format(index))
        self._client.indices.create(index=self._index)
        logger.info('Index created')

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
        logger.info('Adding {} new documents to index'.format(len(docs)))

        for doc in docs:
            for sentence in sentence_split(doc):
                if len(sentence) < 2:
                    continue

                md5 = hashlib.md5()
                md5.update(sentence.lower().encode('utf-8'))

                self._client.index(
                    index=self._index,
                    doc_type='chat_replies',
                    id = md5.hexdigest(),
                    body={'text':sentence}
                )

        logger.info('Documents added')
