"""tools to deal with function launched by the user """

import tkcode.settings


class Command:
    """Base class for commands meant to be displayed in the palette """

    def __init__(
        self,
        name,
        category="",
        title="",
        description="",
        shortcut="",
        command_callable=None,
    ):
        self.name = name
        self.title = title
        self.description = description
        self.shortcut = shortcut
        # callable
        self.command_callable = command_callable

    def __call__(self, app, *args, **kwargs):
        """Execute the callable self.command"""
        self.command_callable(app, *args, **kwargs)


class Commander:
    """A class that handle execution of command instance. """

    COMMANDS = []

    COMMAND_DICT = {}

    def __init__(self, app):
        self.app = app
        self.history = []
        # self.build_commands()

    @classmethod
    def add_command(cls, cmd):
        """register a command"""
        cls.COMMANDS.append(cmd)
        cls.COMMAND_DICT[cmd.name] = cmd

    def run(self, cmd, *args, **kwargs):
        """Execute a command and add it to the history"""
        if isinstance(cmd, str):
            cmd = self.COMMAND_DICT[cmd]
        cmd(self.app, *args, **kwargs)
        self.history.append((cmd, args, kwargs))


def command(category="", title="", description="", shortcut=""):
    """a decorator to register commentsands"""

    def _register_decorator(func):
        """wrapper"""
        Commander.add_command(
            Command(
                func.__name__,
                category,
                title,
                description,
                shortcut,
                command_callable=func,
            )
        )
        return func

    return _register_decorator
