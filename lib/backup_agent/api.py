from typing import Dict

from requests import Response

from lib.abstract_api import AbstractApi


class BackupAgentApi(AbstractApi):
    PLANS = "/plans/"
    DELETE_PLAN = "/plans/{}"
    GET_RESTORE_POINTS = "/plans/{}/restore_points"
    RUN_BACKUP = "/plans/{}/backup"

    GET_TASK = "/tasks/{}"

    def create_plan(self, data: Dict) -> Response:
        """
        :param data: {"name": "name", "paths": ["path1", "path2", ...]}
        """
        return self._session.post(self._host + self.PLANS, json=data)

    def delete_plan(self, plan_id: str) -> Response:
        return self._session.delete(self._host + self.DELETE_PLAN.format(plan_id))

    def get_plans(self) -> Response:
        return self._session.get(self._host + self.PLANS)

    def get_restore_points(self, plan_id: str) -> Response:
        return self._session.get(self._host + self.GET_RESTORE_POINTS.format(plan_id))

    def get_task(self, task_id: str) -> Response:
        return self._session.get(self._host + self.GET_TASK.format(task_id))

    def run_backup(self, plan_id: str) -> Response:
        return self._session.post(
            self._host + self.RUN_BACKUP.format(plan_id),
        )
