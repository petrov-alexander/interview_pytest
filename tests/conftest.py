pytest_plugins = ["tests.fixtures.api"]


def pytest_addoption(parser):
    parser.addoption(
        "--application-host",
        help="Application host for testing",
        dest="application_host",
        required=True,
        action="store",
    )
    parser.addoption(
        "--backup-agent-host",
        help="Backup agent host for testing",
        dest="backup_agent_host",
        required=True,
        action="store",
    )
