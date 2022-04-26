from cleo import Command as CleoCommand


class Command(CleoCommand):
    pass


class Commands:
    @classmethod
    def load(cls):
        return [cmd() for cmd in Command.__subclasses__()]