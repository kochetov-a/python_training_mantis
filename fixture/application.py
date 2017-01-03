from selenium import webdriver
from fixture.session import SessionHelper
from fixture.project import ProjectHelper


class Application:
    # запуск браузера
    def __init__(self, browser, base_url):
        if browser == "firefox":
            self.wd = webdriver.Firefox()
        elif browser == "chrome":
            self.wd = webdriver.Chrome()
        elif browser == "ie":
            self.wd = webdriver.Ie()
        else:
            raise ValueError("Unrecognized browser %s" % browser)
        self.session = SessionHelper(self)
        self.base_url = base_url
        self.project = ProjectHelper(self)

    # проверка валидности фикстуры
    def is_valid(self):
        try:
            self.wd.current_url  # Если браузер может вернуть адрес страницы
            return True  # То фикстура валидна
        except:
            return False

    # открытие главной страницы
    def open_home_page(self):
        wd = self.wd
        wd.get(self.base_url)

    # разрушение фикстуры
    def destroy(self):
        self.wd.quit()