from abc import abstractmethod


class AbstractCommand(object):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def help(self) -> str:
        pass

    @abstractmethod
    def execute(self):
        pass
