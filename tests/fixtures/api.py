import pytest

from lib.application.api import ApplicationApi
from lib.backup_agent.api import BackupAgentApi


@pytest.fixture(scope="session")
def ba_api(request):
    return BackupAgentApi(request.config.option.backup_agent_host)


@pytest.fixture(scope="session")
def app_api(request):
    return ApplicationApi(request.config.option.application_host)
