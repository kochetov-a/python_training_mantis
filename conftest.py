import pytest
from fixture.application import Application
import json
import os.path

fixture = None
target = None


def load_config(file):
    global target  # Объявление глобальной переменной для файла конфигурации
    if target is None:
        # Получаем месторасположение конфига из переменной __file__ и объеденяем его с "target.json"
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:  # Пробуем открыть файл конфигурации и присвоить его переменной "f"
            target = json.load(f)  # Загружаем в переменную "target" содержимое файла
    return target


# Фикстура логина на сайт с проверкой валидности фикстуры
@pytest.fixture
def app(request):
    global fixture  # Объявление глобальной переменной для фикстуры
    web_config = load_config(request.config.getoption("--target"))["web"]
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=web_config["browser"], base_url=web_config["baseUrl"])
    # Открываем главную страницу в любом случае
    fixture.open_home_page()
    # Выполняем логин в любом случае
    return fixture


# Фикстура выхода из приложения
@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        # Убеждаемся что пользователь вылогинился
        fixture.session.ensure_logout()
        # Разрушаем фикстуру
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

# Парсер ключей из командной строки
def pytest_addoption(parser):
    parser.addoption("--target", action="store", default="target.json")
    parser.addoption("--browser", action="store", default="target.json")