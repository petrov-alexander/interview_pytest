import uuid
import allure

from lib.backup_agent.task_states import TaskStates
from waiting import wait


PLAN_NAME = f"test_{str(uuid.uuid4())[:4]}"


@allure.feature("Check duration")
class TestCheckDuration:
    @allure.title("Prepare backups")
    def test_perform_backups(self, ba_api, app_api):
        with allure.step("Plan created"):
            request_data = {"name": PLAN_NAME, "paths": ["test1"]}
            res = ba_api.create_plan(data=request_data)
            res.raise_for_status()
            plan_id = res.json()["id"]
        with allure.step("Application data generated"):
            app_data = {"test1": "data1"}
            res = app_api.update_data(data=app_data)
            res.raise_for_status()
        with allure.step("Run backups"):
            for _ in range(10):
                res = ba_api.run_backup(plan_id=plan_id)
                res.raise_for_status()
                task = res.json()
                task_id = task["id"]
                wait(
                    lambda: ba_api.get_task(task_id=task_id).json()["state"] != TaskStates.IN_PROGRESS,
                    timeout_seconds=10,
                    waiting_for=f"backup task {task_id} completed",
                )
                res = ba_api.get_task(task_id=task_id)
                res.raise_for_status()
                assert res.json()["state"] == TaskStates.COMPLETED

    @allure.title("Count performance statistic")
    def test_count_statistic(self, ba_api, app_api):
        pass
