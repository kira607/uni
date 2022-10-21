from cleo.application import Application

from .commands import Commands


class UniCliApp(Application):
    def __init__(self, *args, **kwargs):
        super(UniCliApp, self).__init__(*args, **kwargs)
        commands = Commands.load()
        for command in commands:
            self.add(command)
