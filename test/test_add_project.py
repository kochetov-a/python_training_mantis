# -*- coding: utf-8 -*-

# Проверка добавления нового проекта
def test_add_project(app, db, json_project, check_ui):
    project = json_project  # Данные для создания нового проекта
    old_projects_from_db = db.get_project_list()   # Получение списка проектов из БД до добавления
    app.project.create(project)     # Создание нового проекта с тестовыми данными
    new_project_from_db = db.get_project_list()     # Получение списка проектов из БД после добавления
    old_projects_from_db.append(project)    # Добавляем в старый список новый проект
    # Сравниваем отсортированные по полю "name" списки проектов
    assert sorted(old_projects_from_db, key=lambda p: p.name) == sorted(new_project_from_db, key=lambda p: p.name)
    if check_ui:    # Включение проверки графического интерфейса при наличии ключа "--check_ui"
        old_projects_from_ui = app.project.get_project_list()   # Получение списка проектов из UI
        del old_projects_from_ui[0]  # Удаляем из списка проектов заголовок таблицы
        # Сравниваем отсортированные по полю "name" списки проектов
        assert sorted(new_project_from_db, key=lambda p: p.name) == sorted(old_projects_from_ui, key=lambda p: p.name)