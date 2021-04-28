from Commands import *


class CommandFactory(object):
    class __HelpCommand(AbstractCommand):
        def __init__(self, factory):
            self.__factory = factory

        @property
        def name(self) -> str:
            return 'HELP'

        @property
        def help(self) -> str:
            return 'Prints this help.'

        def can_execute(self, command: str) -> bool:
            return command == self.name

        def execute(self):
            for command in self.__factory.commands:
                print(f'{command.name}: {command.help}')

    class __UnknownCommand(AbstractCommand):
        def __init__(self):
            self.__command = None

        @property
        def name(self) -> str:
            raise NotImplementedError

        @property
        def help(self) -> str:
            raise NotImplementedError

        def can_execute(self, command: str) -> bool:
            self.__command = command
            return True

        def execute(self):
            print(f'Unknown command: "{self.__command}".')

    def __init__(self):
        self.commands = [
            EchoCommand(),
            GetProductCommand(),
            ReadFileCommand(),
            self.__HelpCommand(self),
        ]

    def get_command(self, line: str) -> AbstractCommand:
        for command in self.commands + [self.__UnknownCommand()]:
            if command.can_execute(line):
                return command
