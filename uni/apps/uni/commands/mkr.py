import os
import json

from uni.apps.report_creator.config import Config
from ._command import Command


class MakeReportCommand(Command):
    '''
    Make report

    mkr
        {path=. : where to make report}
        {dirname=report : report folder name}
        {name=report : report file name}
        {--m|mock : mock creation with default parameters}
    '''

    def handle(self):
        folder = self.argument('path')
        dirname = self.argument('dirname')
        name = self.argument('name')

        path = os.path.abspath(os.path.join(folder, dirname))
        self.line(f'Creating report at: <fg=green>{path}</>')

        from uni.apps import ReportCreator
        rc = ReportCreator()
        config = self.make_config(path, name)
        rc.create_report(config)

    def make_config(self, path, name):
        from uni.locations import data_folder

        cfg = Config(path, name)

        if self.option('mock'):
            return cfg.mock().lock()

        templates = os.listdir(os.path.join(data_folder, 'templates'))
        finished = False
        while not finished:
            cfg.template = self.choice(cfg.template.prompt, templates, 0)
            cfg.department = self.ask(cfg.department.question)
            cfg.label = self.ask(cfg.label.question)
            cfg.num = self.ask(cfg.num.question)
            cfg.discipline = self.ask(cfg.discipline.question)
            cfg.theme = self.ask(cfg.theme.question)
            cfg.partners = self.ask(cfg.partners.question)
            cfg.teacher = self.ask(cfg.teacher.question)
            cfg.year = self.ask(cfg.year.question)
            cfg.chapters = self.ask(cfg.chapters.question)
            cfg.newpage = self.confirm(cfg.newpage.prompt, cfg.newpage.default)

            data = json.dumps(cfg.dict(), indent=4, skipkeys=True, ensure_ascii=False)
            finished = self.confirm(f'Your input:\n{data}\ncontinue?:')

        return cfg.lock()
