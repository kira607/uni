import datetime
import json

from typing import Type


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
        self.prompt = prompt
        self.optional = optional
        self.default = default

    def __get__(self, obj, objtype=None):
        return self.value

    def __set__(self, obj, val):
        self.value = val


class Config:
    # teplate config
    template = ConfigField('template', 'Шаблон отчёта', optional=True, default='latex-template-v2')

    # header
    department = ConfigField('department', 'Кафедра')

    # main
    label = ConfigField('label', 'Тип работы', optional=True, default='ОТЧЁТ\\\\ЛАБОРАТОРНАЯ РАБОТА')
    num = ConfigField('num', 'Номер работы', type_=int, optional=True, default=None)
    discipline = ConfigField('discipline', 'Дисциплина')
    theme = ConfigField('theme', 'Тема работы')

    # footer
    partners = ConfigField('partners', 'Партнёры', type_=list)
    teacher = ConfigField('teacher', 'Преподаватель Фамилия И.О.')
    year = ConfigField('year', 'Год', optional=True, default=datetime.datetime.now().year)

    # chapters
    chapters = ConfigField('chapters', 'Главы', type_=dict, optional=True, default={})

    # other
    newpage = ConfigField('newpage', 'Новая страница к каждой главе', type_=bool, optional=True, default=True)

    def __init__(self):
        self.config = None

    def fields(self):
        pass

    def load(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.config = json.loads(content)
        except Exception as e:
            print(f'could not load config: {e}')
            raise

        self.template = self.get_value('template')

        self.dest_path = self.get_value('dest_path')
        self.dir_name = self.get_value('dir_name')
        self.report_name = self.get_value('report_name')

        self.department = self.get_value('department')
        self.label = self.get_value('label')
        self.num = self.get_value('num', optional=True, default=None)
        self.discipline = self.get_value('discipline')
        self.theme = self.get_value('theme')

        self.partners = self.get_value('partners', optional=True, default=None)
        self.teacher = self.get_value('teacher')
        self.year = self.get_value('year')

        self.sectioning = self.get_value('sectioning', optional=True, default='\\section*')
        self.chapters = self.get_value('chapters', optional=True, default={})

        self.newpage = self.get_value('newpage', optional=True, default=True)


    def get_value(self, key, optional=False, default=None):
        print(f'Key {key}: ', end='')
        value = self.config.get(key, _MISSING)
        if value == _MISSING:
            if optional:
                print(default)
                return default
            print(_MISSING)
            raise MissingError(f'The config missing key: {key}')
        print(value)
        return value

    def _get_sem(self):
        now = datetime.datetime.now()
        year = now.year
        month = now.month
        sem = (year - 2019) * 2
        sem -= 1 if  month >= 9 else 0
        return sem