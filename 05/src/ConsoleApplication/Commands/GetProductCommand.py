from Commands import AbstractCommand


class GetProductCommand(AbstractCommand):
    @property
    def name(self):
        return 'GET_PRODUCT'

    @property
    def help(self) -> str:
        return 'Calculates the product of the given values.'

    @property
    def arguments(self) -> list:
        return ['first', 'second']

    def execute(self, options: dict):
        print(f'{int(options["first"]) * int(options["second"])}')
