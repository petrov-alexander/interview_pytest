import uuid

import allure

from lib.backup_agent.errors import Errors
from lib.backup_agent.task_states import TaskStates
from waiting import wait

from lib.backup_agent.task_types import TaskTypes

import pendulum


@allure.feature("Run backup")
class TestRunBackup:
    @allure.title("Run backup with valid data")
    def test_run_backup(self, ba_api, app_api):
        with allure.step("Plan created"):
            request_data = {"name": "test", "paths": ["test1", "test2", "test4"]}
            res = ba_api.create_plan(data=request_data)
            assert res.status_code == 201
            plan_id = res.json()["id"]
        with allure.step("Application data generated"):
            app_data = {"test1": "data1", "test2": "data2", "test3": "data3"}
            res = app_api.update_data(data=app_data)
            assert res.status_code == 200
        with allure.step("Run backup"):
            res = ba_api.run_backup(plan_id=plan_id)
        with allure.step("Check backup in progress"):
            assert res.status_code == 200
            task = res.json()
            assert task["id"] is not None
            assert task["plan_id"] == plan_id
            assert task["state"] == TaskStates.IN_PROGRESS
            assert task["error"] is None
            assert task["type"] == TaskTypes.BACKUP
            assert task["paths"] == request_data["paths"]
            assert pendulum.parse(task["start_time"]).diff(pendulum.now()).in_seconds() < 5
            assert task["finish_time"] is None
            task_id = task["id"]
        with allure.step("Wait backup task completed"):
            wait(
                lambda: ba_api.get_task(task_id=task["id"]).json()["state"]
                        != TaskStates.IN_PROGRESS,
                timeout_seconds=10,
                waiting_for=f"backup task {task_id} completed",
            )
        with allure.step("Backup completed successfully"):
            res = ba_api.get_task(task_id=task_id)
            assert res.status_code == 200
            task = res.json()
            assert task["id"] is not None
            assert task["plan_id"] == plan_id
            assert task["state"] == TaskStates.COMPLETED
            assert task["error"] is None
            assert task["type"] == TaskTypes.BACKUP
            assert task["paths"] == request_data["paths"]
            assert pendulum.parse(task["start_time"]) < pendulum.parse(task["finish_time"])
            assert pendulum.parse(task["finish_time"]).diff(pendulum.now()).in_seconds() < 5

    @allure.title("Run backup with not existing plan")
    def test_run_backup_with_not_existing_plan(self, ba_api, app_api):
        with allure.step("Run backup with not existing plan"):
            res = ba_api.run_backup(plan_id=str(uuid.uuid4()))
        with allure.step("Check backup in progress"):
            assert res.status_code == 404
            data = res.json()
            assert data["code"] == Errors.PLAN_NOT_FOUND
