import datetime
import json

from typing import Type


class __MISSING(object):
    def __str__(self):
        return '_MISSING'

    def __repr__(self):
        return str(self)


_MISSING = __MISSING()


class MissingError(Exception):
    pass


class ConfigField:
    def __init__(self, name: str, prompt: str, type_: Type = str, optional: bool = False, default: bool = None):
        self._name = name
        self._type = type_
        self._value: type_ = None
        self._prompt = prompt
        self._optional = optional
        self._default = default

    @property
    def value(self):
        return self._value

    def input(self):
        prompt = self._prompt
        if self._optional:
            prompt += f' (hit Enter to use default: "{self._default}")'
        prompt += ':'
        value = self._input(prompt)
        if not value or value == '':
            value = self._default
        self._value = value

    def _input(self, prompt):
        if self._type == str:
            return input(prompt)
        if self._type == int:
            return int(input(prompt))
        elif self._type == list:
            l = []
            v = None
            i = 1
            while v != '':
                v = input(f'{i} - {prompt}')
                if v != '':
                    l.append(v)
                    i += 1
            return l
        elif self._type == dict:
            d = {}
            k, v = None, None
            i = 1
            while k != '':
                k = input(f'{i} - {prompt}')
                v = input(f'{i} - {prompt}')
                if k != '':
                    d[k] = v
                    i += 1
        elif self._type == bool:
            v = ''
            while not(v == 'True' or v == 'False'):
                v = input(prompt)
            return True if v == 'True' else False



class Config:
    def __init__(self):
        self.config = None

        # teplate config
        self.template = ConfigField('template', 'Шаблон отчёта', optional=True, default='latex-template-v2')

        # file config
        self.sem = ConfigField('sem', 'Семестр', type_=int, optional=True, default=self._get_sem())
        self.dest_path = ConfigField('dest_path', 'Папка назначения')
        self.dir_name = ConfigField('dir_name', 'Название папки')
        self.report_name = ConfigField('report_name', 'Название отчёта')

        # report config
        self.department = ConfigField('department', 'Кафедра')
        self.label = ConfigField('label', 'Тип работы', optional=True, default='ОТЧЁТ\\\\ЛАБОРАТОРНАЯ РАБОТА')
        self.num = ConfigField('num', 'Номер работы', type_=int, optional=True, default=None)
        self.discipline = ConfigField('discipline', 'Дисциплина')
        self.theme = ConfigField('theme', 'Тема работы')
        self.partners = ConfigField('partners', 'Партнёры', type_=list)
        self.teacher = ConfigField('teacher', 'Преподаватель Фамилия И.О.')
        self.year = ConfigField('year', 'Год', optional=True, default=datetime.datetime.now().year)
        self.chapters = ConfigField('chapters', 'Главы', type_=dict, optional=True, default={})

        # other
        self.newpage = ConfigField('newpage', 'Новая страница к каждой главе', type_=bool, optional=True, default=True)

    def __getattr__(self, name):
        field = getattr(self, name)
        if isinstance(field, ConfigField):
            return field.value
        else:
            return super(ConfigField, self).__getattr__(name)

    @property
    def template_path(self):
        return f'templates/{self.template}/'

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

    def input(self):
        self.sem.input()
        self.template.input()
        self.dest_path.input()
        self.dir_name.input()
        self.report_name.input()
        self.department.input()
        self.label.input()
        self.num.input()
        self.discipline.input()
        self.theme.input()
        self.partners.input()
        self.teacher.input()
        self.year.input()
        self.sectioning.input()
        self.chapters.input()
        self.newpage.input()


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
        print(now)
        year = now.year
        month = now.month
        print(year)
        print(month)
        sem = (year - 2019) * 2
        sem -= 1 if  month >= 9 else 0
        return sem