# -*- coding: utf-8 -*-

from model.project import Project


# Класс-помощник для работы с проектами
class ProjectHelper:

    def __init__(self, app):
        self.app = app


    # Функция создания нового контакта
    def create(self, project):
        wd = self.app.wd
        self.open_manage_projects_page()
        wd.find_element_by_xpath("//table[@class='width100']//input[@value='Create New Project']").click()
        self.fill_project_form(project)
        wd.find_element_by_xpath("//table[@class='width75']//input[@value='Add Project']").click()
        self.open_manage_projects_page()
        self.project_cache = None

    # Функция открытия страницы управления контактами
    def open_manage_projects_page(self):
        wd = self.app.wd
        wd.find_element_by_link_text("Manage").click()
        wd.find_element_by_link_text("Manage Projects").click()

    # Функция заполнения полей нового контакта
    def fill_project_form(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_field_value("description", project.description)

    # Функция изменения полей проекта
    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:  # Если переменная "text" не пустая,то передаём её значение в поля
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    project_cache = None

    # Получение списка проектов на странице
    def get_project_list(self):
        if self.project_cache is None:  # Если кеш списка контактов пуст, то заполняем его
            wd = self.app.wd
            self.open_manage_projects_page()
            self.project_cache = []  # Создание пустого списка "project"
            for row in wd.find_elements_by_xpath("//table[@class='width100'][@cellspacing='1']//tbody//tr[@class]"):
                cells = row.find_elements_by_tag_name("td")  # Получение содержимого ячеек из строк
                name = cells[0].text  # Имя проекта из ячейки #1
                description = cells[4].text  # Описание проекта из ячейки #2
                self.project_cache.append(Project(name=name, description=description))
        return list(self.project_cache)  # Возвращаем список контактов

