# -*- coding: utf-8 -*-

from sys import maxsize

# Конструктор класса проектов
class Project:

    def __init__(self, name=None, description=None, id=None):
        self.name = name
        self.description = description
        self.id = id

    # Переопределение функции вывода значений для проектов
    def __repr__(self):
        return "%s:%s" % (self.name, self.description)

    # Переопределение функции сравнения проектов
    def __eq__(self, other):
        return self.name == other.name and self.description == other.description

    # Функция возвращает максимальный id или (если он None) максимальное число
    def id_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize
