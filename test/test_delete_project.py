# -*- coding: utf-8 -*-

import random
from model.project import Project


# Удаление случайного проекта из списка
def test_delete_some_project(app, db, check_ui):
    if len(db.get_project_list()) == 0:  # Получаем из БД список проектов, если список пустой, то
        app.project.create(Project(name="Test Name 1", description="Test Description 1"))  # Создаём новый проект
    old_projects_from_db = db.get_project_list()  # Сохранение списка проектов из БД до удаления
    project = random.choice(old_projects_from_db)  # Получение имени случайного проекта для удаления
    app.project.delete_project_by_name(project.name)  # Удаляем проект по полю "name"
    new_project_from_db = db.get_project_list()  # Получение списка проектов из БД после удаления
    old_projects_from_db.remove(project)  # Удаляем выбранный проект из старого списка
    # Сравниваем отсортированные по полю "name" списки проектов
    assert sorted(old_projects_from_db, key=lambda p: p.name) == sorted(new_project_from_db, key=lambda p: p.name)
    if check_ui:  # Включение проверки графического интерфейса при наличии ключа "--check_ui"
        # Сравниваем отсортированные по полю "name" списки проектов
        old_projects_from_ui = app.project.get_project_list()  # Получение списка проектов из UI
        del old_projects_from_ui[0]  # Удаляем из списка проектов заголовок таблицы
        assert sorted(old_projects_from_ui, key=lambda p: p.name) == sorted(new_project_from_db, key=lambda p: p.name)