import logging
from abc import ABC

import requests
from requests import Response


class AbstractApi(ABC):
    def __init__(self, host: str):
        self._host = host
        self._session = requests.Session()
        self.logger = logging.getLogger(self.__class__.__name__)
        self._session.hooks.update(
            {"response": [self._request_logging, self._response_logging]}
        )

    def _request_logging(self, r: Response, *args, **kwargs):
        self.logger.info(
            f"Request: {r.request.method} {r.request.url} {r.request.body}"
        )

    def _response_logging(self, r: Response, *args, **kwargs):
        self.logger.info(f"Response: {r.request.method} {r.url} {r.content}")
