from cleo import Application

from .commands import Commands


class UniApp(Application):
    def __init__(self, *args, **kwargs):
        super(UniApp, self).__init__(*args, **kwargs)
        cmds = Commands.load()
        for cmd in cmds:
            self.add(cmd)
