import mysql.connector
from model.project import Project


# Класс для работы с базой данных
class DbFixture():


    def __init__(self, host, name, user, password):  # Инициализация параметров подключения к БД
        self.host = host
        self.name = name
        self.user = user
        self.password = password
        self.connection = mysql.connector.connect(host=host, database=name, user=user, password=password)
        self.connection.autocommit = True  # Отключение кэширования в базе данных


    # Получение списка групп из базы данных из таблицы "group_list"
    def get_project_list(self):
        list = []
        cursor = self.connection.cursor()
        try:  # Пробуем выполнить запрос к БД
            # Получение данных проектов
            cursor.execute("select name, description from mantis_project_table")
            for row in cursor:
                (name, description) = row
                list.append(Project(name=name, description=description))
        finally:
            cursor.close()
        return list

    # Функция для разрыва соеденения с БД
    def destroy(self):
        self.connection.close()