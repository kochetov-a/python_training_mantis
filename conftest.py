import pytest
from fixture.application import Application
from fixture.db import DbFixture
import json
import os.path
import jsonpickle
import json
import os.path
import importlib

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
    fixture.session.ensure_login(username=web_config["username"], password=web_config["password"])
    return fixture


# Фикстура для подключения базы данных
@pytest.fixture(scope="session")
def db(request):
    db_config = load_config(request.config.getoption("--target"))["db"]
    dbfixture = DbFixture(host=db_config["host"], name=db_config["name"], user=db_config["user"],
                          password=db_config["password"])
    def fin():
        dbfixture.destroy()
    request.addfinalizer(fin)
    return dbfixture


@pytest.fixture
def check_ui(request):
    return request.config.getoption("--check_ui")

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
    parser.addoption("--check_ui", action="store_true")

# Генератор тестов для динамической подстановки параметров
def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            test_data = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])
        elif fixture.startswith("json_"):
            test_data = load_from_json(fixture[5:])
            metafunc.parametrize(fixture, test_data, ids=[str(x) for x in test_data])


# Импортируем тестовые данные из файла .py с тестовыми данными (groups.py или contacts.py)
def load_from_module(module):
    return importlib.import_module("data.%s" % module).data_for_contact


# Получаем тестовые данные из json-файла (groups.json или contacts.json)
def load_from_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())  # Читаем файл json