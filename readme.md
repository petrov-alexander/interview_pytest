# Тесты на Pytest
В репозитории реализованы некоторые API тесты на Pytest для сервиса https://github.com/petrov-alexander/interview_service

## Подготовка
```bash
python -m venv venv

# для Linux
source venv/bin/activate
# или для Windows
venv/Scripts/activate

pip install -r requirements.txt
```

## Запуск
```bash
# --backup-agent-host - адрес хоста бэкап агента
# --application-host  - адрес хоста приложения, данные которого бэкапим
# --alluredir         - директория для формирования allure отчета
# например:
pytest --backup-agent-host=http://localhost:8000 --application-host=http://localhost:8000 tests/test_plan/test_create_plan.py
```
