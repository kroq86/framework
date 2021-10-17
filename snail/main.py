import re
from typing import Type,List
from snail.exceptions import NotFound
from snail.view import View
from snail.exceptions import NotAllowed
from snail.urls import Url

class Snail:

    __slots__ = 'urls',

    def __init__(self, urls: List[Url]):
        self.urls = urls

    def _prepare_url(self, url: str):
        if url[-1] == '/':
            return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        url = self._prepare_url(raw_url)
        for path in self.urls:
            m = re.match(path.url, url)
            if m is not None:
                return path.view
        raise NotFound

    def __call__(self, environ, start_response, **kwargs):
        print(environ)
        raw_url = environ["PATH_INFO"]
        view = self._find_view(raw_url)()
        method = environ["REQUEST_METHOD"].lower()
        if not hasattr(view, method):
            raise NotAllowed
        raw_response = getattr(view, method)(None)
        response = raw_response.encode('utf-8')
        start_response("200 OK", [
            ("Content-Type", "text/plain"),
            ("Content-Length", str(len(response)))
        ])
        return iter([response])