import os
import json

from uni.report_creator.config import Config
from ._command import Command


class MakeReportCommand(Command):
    '''
    Make report

    mkr
        {path=. : where to make report}
        {dirname=report : report folder name}
        {name=report : report file name}
        {--m|mock : mock creation with default parameters}
        {--c|config-file= : create report form config file instead of interactive input}
    '''

    def handle(self):
        folder = self.argument('path')
        dirname = self.argument('dirname')
        name = self.argument('name')

        path = os.path.abspath(os.path.join(folder, dirname))
        self.line(f'Creating report at: <fg=green>{path}</>')

        from uni.report_creator import ReportCreator
        rc = ReportCreator()
        config = self.make_config(path, name)
        rc.create_report(config)

    def make_config(self, path, name):
        cfg = Config(path, name)

        if self.option('mock'):
            cfg.mock()
        elif self.option('config-file'):
            self.load_config(cfg)
        else:
            self.input_config(cfg)

        return cfg.lock()

    def load_config(self, cfg):
        with open(self.option('config-file'), 'r') as f:
            data = json.load(f)
            cfg.load(data)

    def input_config(self, cfg):
        from uni.locations import data_folder
        templates = os.listdir(os.path.join(data_folder, 'templates'))
        finished = False

        while not finished:
            cfg.template = self.choice(cfg.template.prompt, templates, 0)
            cfg.department = self.ask(cfg.department.question)
            cfg.label = self.ask(cfg.label.question)
            cfg.num = self.ask(cfg.num.question)
            cfg.discipline = self.ask(cfg.discipline.question)
            cfg.theme = self.ask(cfg.theme.question)

            partners_num_q = self.create_question('Кол-во партнёров [0]:', default=0)
            partners_num_q.set_validator(int)
            partners_num = self.ask(partners_num_q)

            self.line(f'{partners_num}')
            if partners_num == 0:
                cfg.partners = []

            for i in range(partners_num):
                p = self.ask(f'Партнёр #{i+1}:')
                cfg.partners.value.append(p)

            cfg.teacher = self.ask(cfg.teacher.question)
            cfg.year = self.ask(cfg.year.question)

            chapter = 'any'
            while chapter:
                chapter_file = self.ask('Глава (имя файла) [None]:', default=None)
                if not chapter_file:
                    break
                chapter_name = self.ask(f'Глава (название) [{chapter_file}]:', default=chapter_file)
                cfg.chapters.value[chapter_file] = chapter_name

            cfg.newpage = self.confirm(cfg.newpage.prompt, cfg.newpage.default)

            data = json.dumps(cfg.dict(), indent=4, skipkeys=True, ensure_ascii=False)
            finished = self.confirm(f'Your input:\n{data}\ncontinue?:', default=True)

