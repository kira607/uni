from abc import ABC

from cleo.commands.command import Command as CleoCommand


class Command(CleoCommand, ABC):
    pass


class Commands:
    @classmethod
    def load(cls):
        return [cmd() for cmd in Command.__subclasses__()]
