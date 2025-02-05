import uuid

import allure

from lib.backup_agent.errors import Errors
from lib.backup_agent.states import States
from waiting import wait


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
            backup = res.json()
            assert backup["id"] is not None
            assert backup["plan_id"] == plan_id
            assert backup["state"] == States.IN_PROGRESS
            assert backup["error"] is None
            backup_id = backup["id"]
        with allure.step("Wait backup completed"):
            wait(
                lambda: ba_api.get_backup(backup_id=backup["id"]).json()["state"]
                != States.IN_PROGRESS,
                timeout_seconds=10,
                waiting_for=f"backup {backup_id} completed",
            )
        with allure.step("Backup completed successfully"):
            res = ba_api.get_backup(backup_id=backup_id)
            assert res.status_code == 200
            backup = res.json()
            assert backup["id"] is not None
            assert backup["plan_id"] == plan_id
            assert backup["state"] == States.COMPLETED
            assert backup["error"] is None
        with allure.step("Restore point created correctly"):
            res = ba_api.get_restore_points(plan_id=plan_id)
            assert res.status_code == 200
            rps = res.json()
            assert len(rps) == 1
            assert len(rps["1"]) == 2
            assert rps["1"]["test1"] == "data1"
            assert rps["1"]["test2"] == "data2"

    @allure.title("Run backup with not existing plan")
    def test_run_backup_with_not_existing_plan(self, ba_api, app_api):
        with allure.step("Run backup with not existing plan"):
            res = ba_api.run_backup(plan_id=str(uuid.uuid4()))
        with allure.step("Check backup in progress"):
            assert res.status_code == 404
            data = res.json()
            assert data["code"] == Errors.PLAN_NOT_FOUND
