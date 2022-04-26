import os

from uni.apps.report_creator.config import Config
from ._command import Command


class MakeReportCommand(Command):
    '''
    Make report

    mkr
        {path=. : where to make report}
        {name=report : report folder name}
    '''

    def handle(self):
        folder = self.argument('path')
        name = self.argument('name')
        path = os.path.abspath(os.path.join(folder, name))
        self.line(f'Creating report at: <fg=green>{path}</>')
        from uni.apps import ReportCreator
        rc = ReportCreator()
        config = self.make_config(path)
        # rc.create_report(path)

    def make_config(self, path):
        from uni.locations import data_folder

        cfg = Config()

        templates = os.listdir(os.path.join(data_folder, 'templates'))
        cfg.template = self.choice('template', templates, 0)
        cfg.