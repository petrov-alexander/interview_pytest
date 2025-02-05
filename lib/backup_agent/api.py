from typing import Dict

from requests import Response

from lib.abstract_api import AbstractApi


class BackupAgentApi(AbstractApi):
    CREATE_PLAN = "/plans"
    DELETE_PLAN = "/plans/{}"
    GET_RESTORE_POINTS = "/plans/{}/restore_points"

    RUN_BACKUP = "/backups"
    GET_BACKUP = "/backups/{}"

    def create_plan(self, data: Dict) -> Response:
        """
        :param data: {"name": "name", "paths": ["path1", "path2", ...]}
        """
        return self._session.post(self._host + self.CREATE_PLAN, json=data)

    def delete_plan(self, plan_id: str) -> Response:
        return self._session.delete(self._host + self.DELETE_PLAN.format(plan_id))

    def get_restore_points(self, plan_id: str) -> Response:
        return self._session.get(self._host + self.GET_RESTORE_POINTS.format(plan_id))

    def run_backup(self, plan_id: str) -> Response:
        return self._session.post(
            self._host + self.RUN_BACKUP, json={"plan_id": plan_id}
        )

    def get_backup(self, backup_id: str) -> Response:
        return self._session.get(self._host + self.GET_BACKUP.format(backup_id))
