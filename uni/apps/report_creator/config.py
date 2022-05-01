import datetime
import json
import os
from os.path import abspath, join

from typing import Type
from clikit.ui.components import Question, ChoiceQuestion
from uni.locations import data_folder

class __MISSING(object):
    def __str__(self):
        return '_MISSING'

    def __repr__(self):
        return str(self)

    def __copy__(self):
        return self

    def __deepcopy__(self):
        return self


_MISSING = __MISSING()


class MissingError(Exception):
    pass


class ConfigField:
    def __init__(self, name: str, prompt: str, type_: Type = str, optional: bool = False, default: str = None):
        self.name = name
        self.type = type_
        self.value: type_ = default if optional else None
        self._prompt = prompt
        self.optional = optional
        self.default = default
        self._get = self

    @property
    def question(self):
        q = Question(self.prompt, self.default)
        return q

    @property
    def prompt(self):
        prompt = self._prompt
        if self.optional:
            prompt += f' [{self.default}]'
        prompt += ':'
        return prompt

    def lock(self):
        self._get = self.value

    def __get__(self, obj, objtype=None):
        return self._get

    def __set__(self, obj, val):
        self.value = val


class Config:
    template = ConfigField('template', 'Шаблон отчёта', optional=True, default='full_template')
    department = ConfigField('department', 'Кафедра', optional=True, default='САПР')
    label = ConfigField('label', 'Тип работы', optional=True, default=r'ОТЧЁТ\\ЛАБОРАТОРНАЯ РАБОТА')
    num = ConfigField('num', 'Номер работы', type_=int, optional=True, default=None)
    discipline = ConfigField('discipline', 'Дисциплина', optional=True, default=None)
    theme = ConfigField('theme', 'Тема работы', optional=True, default=None)
    student = ConfigField('student', '')
    partners = ConfigField('partners', 'Партнёры', type_=list, optional=True, default=None)
    teacher = ConfigField('teacher', 'Преподаватель Фамилия И.О.')
    year = ConfigField('year', 'Год', optional=True, default=datetime.datetime.now().year)
    chapters = ConfigField('chapters', 'Главы', type_=dict, optional=True, default={})
    newpage = ConfigField('newpage', 'Новая страница к каждой главе', type_=bool, optional=True, default=True)

    def __init__(self, path: str, name: str):
        self.path = path
        self.name = f'{name}.tex'
        self.locked = False
        self.sectioning = '\\section'
        self.d = {}

    @property
    def template_path(self):
        return os.path.abspath(os.path.join(data_folder, 'templates', self.template))

    @property
    def main_page_path(self):
        return abspath(join(self.path, self.name))

    @property
    def title_page_path(self):
        return abspath(join(self.path, 'modules', 'title_page.tex'))

    @property
    def report_dir(self):
        return self.path
    
    def lock(self):
        self.d = self.dict()
        for field in self.fields():
            if field.name == 'num':
                field.value = f' №{field.value}'
            elif field.name == 'student':
                field.value = 'Студенты' if self.partners.value else 'Студент '
            field.lock()
        return self

    def fields(self):
        fs = []
        for n, f in self.__class__.__dict__.items():
            if isinstance(f, ConfigField):
                fs.append(f)
        return fs

    def dict(self):
        if self.locked:
            return self.d
        self.d = {}
        for f in self.fields():
            self.d[f.name] = f.value
        return self.d

    def load(self, data: dict):
        self.template = self.get_value(data, 'template', self.template)
        self.department = self.get_value(data, 'department', self.department)
        self.label = self.get_value(data, 'label', self.label)
        self.num = self.get_value(data, 'num', self.num)
        self.discipline = self.get_value(data, 'discipline', self.discipline)
        self.theme = self.get_value(data, 'theme', self.theme)
        self.student = self.get_value(data, 'student', self.student)
        self.partners = self.get_value(data, 'partners', self.partners)
        self.teacher = self.get_value(data, 'teacher', self.teacher)
        self.year = self.get_value(data, 'year', self.year)
        self.chapters = self.get_value(data, 'chapters', self.chapters)
        self.newpage = self.get_value(data, 'newpage', self.newpage)

    def get_value(self, data, key, field):
        value = data.get(key, _MISSING)
        if value == _MISSING:
            if field.optional:
                return field.default
            raise MissingError(f'The config missing key: {key}')
        return value

    def mock(self):
        self.template = 'full_template'
        self.num = '0'
        self.discipline = 'Дисциплина'
        self.theme = 'тема'
        self.partners = [] # ['Иванов И.И.', 'Петров П.П.']
        self.teacher = 'Преподаватель'
        self.chapters = {
            'task': 'Задача',
            'solution': 'Решение',
        }
        self.newpage = True
        return self

    def _get_sem(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        sem = (year - 2019) * 2
        sem -= 1 if  month >= 9 else 0
        return sem