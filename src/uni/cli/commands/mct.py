import os
import json

from uni.report_creator.config import Config
from ._command import Command


class MakeConfigTemplateCommand(Command):
    '''
    Create config template file

    mct
        {path=. : where to make config template}
        {name=.report_config.json : name of the config file}
    '''

    def handle(self):
        template = Config.config_template()
        path = self.argument('path')
        name = self.argument('name')
        template_path = os.path.abspath(os.path.join(path, name))
        with open(template_path, 'w', encoding='utf-8') as f:
            json.dump(template, indent=4, fp=f)

