import json
import werkzeug.exceptions
from flask import request
from functools import wraps


class accepts(object):
    def __init__(self, mimetype):
        self._mimetype = mimetype

    def __call__(self, func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            if not request.content_type == self._mimetype:
                raise werkzeug.exceptions.NotFound('Invalid mimetype')

            return func(*args, **kwargs)
        return _wrapper


class params(object):
    def __init__(self, **kwargs):
        self._params = kwargs

    def __call__(self, func):
        @wraps(func)
        def _wrapper():
            extracted_params = {}
            for name,typ in self._params.items():
                extracted_params[name] = typ(request.values[name])
                return func(**extracted_params)

        return _wrapper


class json_serialize(object):
    def __init__(self, encoding='utf-8', headers={}):
        self._encoding = encoding
        self._headers = headers
        self._headers['Content-Type'] = 'application/json; charset={}'.format(self._encoding)

    def __call__(self, func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            body = json.dumps(func(*args, **kwargs)).encode(self._encoding)
            return (body, 200, self._headers)
        return _wrapper
