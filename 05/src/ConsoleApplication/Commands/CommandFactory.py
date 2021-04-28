from Commands import *


class CommandFactory(object):
    def __init__(self):
        self.commands = [
            EchoCommand(),
            GetProductCommand(),
            ReadFileCommand(),
        ]

    def get_command(self, line: str) -> AbstractCommand:
        for command in self.commands:
            if command.name == line:
                return command
