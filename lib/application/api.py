from typing import Dict

from requests import Response

from lib.abstract_api import AbstractApi


class ApplicationApi(AbstractApi):
    DELETE_DATA = "/data"
    GET_DATA = "/data"
    UPDATE_DATA = "/data"

    def delete_data(self) -> Response:
        return self._session.delete(self._host + self.DELETE_DATA)

    def get_data(self) -> Response:
        return self._session.get(self._host + self.DELETE_DATA)

    def update_data(self, data: Dict[str, str]) -> Response:
        return self._session.put(self._host + self.DELETE_DATA, json=data)
