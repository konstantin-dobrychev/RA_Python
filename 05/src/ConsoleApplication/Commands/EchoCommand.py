import sys

from Commands import AbstractCommand


class EchoCommand(AbstractCommand):
    @property
    def name(self):
        return 'ECHO_START'

    @property
    def help(self) -> str:
        return 'Starts an echo loop.'

    @property
    def arguments(self) -> list:
        return []

    def execute(self, _options: dict):
        while True:
            message = sys.stdin.readline()

            if message.strip() == 'ECHO_STOP':
                break

            sys.stdout.write(message)
