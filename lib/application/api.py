from typing import Dict

from requests import Response

from lib.abstract_api import AbstractApi


class ApplicationApi(AbstractApi):
    DATA = "/data"

    def delete_data(self) -> Response:
        return self._session.delete(self._host + self.DATA)

    def get_data(self) -> Response:
        return self._session.get(self._host + self.DATA)

    def update_data(self, data: Dict[str, str]) -> Response:
        return self._session.put(self._host + self.DATA, json=data)
