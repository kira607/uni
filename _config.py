import json


class __MISSING(object):
    def __str__(self):
        return '_MISSING'

    def __repr__(self):
        return str(self)


_MISSING = __MISSING()


class MissingError(Exception):
    pass


class Config:
    def __init__(self):
        self.config = None
        # all default values are given as example

        # teplate config
        self.template = 'latex-template-v2'

        # file config
        self.dest_path = '4_sem/english/'
        self.dir_name = '1-idz'
        self.report_name = '1-English-Leskin-9892'

        # report config
        self.department = 'Иностранных Языков'
        self.label = 'Домашнее задание'
        self.num = 1  # optional
        self.discipline = 'Иностранный язык'
        self.theme = 'Conditional sentences'
        self.partners = None  # optional
        self.teacher = 'Козеличкина Г.В.'
        self.year = '2021'
        self.chapters = {
            'chapter': 'Chapter 1',
            '#144-chapter2': '#\\chapter{chap2}'
        }

        # other
        self.newpage = False

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