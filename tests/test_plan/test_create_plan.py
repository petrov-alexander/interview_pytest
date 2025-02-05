import allure
import pytest


@allure.feature("Create plan")
class TestCreatePlan:
    @allure.title("Create plan with valid data")
    def test_create_plan(self, ba_api):
        with allure.step("Create plan"):
            request_data = {"name": "test", "paths": ["test1", "test2", "test4"]}
            res = ba_api.create_plan(data=request_data)
        with allure.step("Plan created successfully"):
            assert res.status_code == 201
            data = res.json()
            assert data["name"] == request_data["name"]
            assert data["paths"] == request_data["paths"]
            assert data["id"] is not None

    @allure.title("Create plan without {field}")
    @pytest.mark.parametrize("field", ["name", "paths"])
    def test_create_plan_without_required_field(self, ba_api, field):
        with allure.step(f"Create plan without {field}"):
            request_data = {"name": "test", "paths": ["test"]}
            request_data.pop(field)
            res = ba_api.create_plan(data=request_data)
        with allure.step("Error is returned"):
            assert res.status_code == 422
            data = res.json()
            assert data["detail"][0]["msg"] == "Field required"
            assert data["detail"][0]["type"] == "missing"
            assert data["detail"][0]["loc"] == ["body", field]
