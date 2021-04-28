import os

from Commands import AbstractCommand


class ReadFileCommand(AbstractCommand):
    @property
    def name(self) -> str:
        return 'READ_FILE'

    @property
    def help(self) -> str:
        return 'Print the content of the given file.'

    @property
    def arguments(self) -> list:
        return ['filename']

    def execute(self, options: dict):
        filename = options['filename']

        with open(filename, 'rb') as f:
            print(f.read(os.stat(filename).st_size).decode())
