from ._command import Command


class DebugCommand(Command):
    '''
    Debug command

    debug
    '''

    def handle(self):
        from uni.locations import data_folder
        import os
        self.line(f'data folder: <fg=green>{data_folder}</>')
        print(os.getcwd())
        