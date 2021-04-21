from DeviceMode import DeviceMode
from typing import List


class Device(object):
    _devices = {
        '/devices/dev0': (DeviceMode.ReadOnly, ['line_1', 'line_2']),
        '/devices/dev1': (DeviceMode.WriteOnly, ['']),
        '/devices/dev2': (DeviceMode.ReadWrite, []),
        '/devices/dev3': (DeviceMode.ReadWrite, ['1', '2', '**', 'hello', '']),
        '/devices/dev4': (DeviceMode.ReadOnly, ['line_1', 'line_2']),
    }

    def __init__(self, mode=DeviceMode.ReadOnly, data=None):
        self.__mode = mode
        self.__data = data

    @property
    def mode(self):
        return self.__mode

    def is_readable_device(self) -> bool:
        """Показывает, можно ли читать из устройства."""
        return DeviceMode.ReadOnly in self.__mode

    def is_writable_device(self) -> bool:
        """Показывает, можно писать в устройство."""
        return DeviceMode.WriteOnly in self.__mode

    @classmethod
    def open_device(cls, name: str):
        """
        Открывает указанное устройство.
        :param name: имя устройства
        :return: открытое устройство
        :exception KeyError если устройство не зарегистрировано в таблице
        """
        try:
            mode, data = cls._devices[name]
            return Device(mode, data)
        except KeyError:
            raise IOError('Device no found')

    def read_line(self) -> str:
        """
        Читает строку текста из устройства
        :param device: устройство
        :return: считанная строка
        :exception IndexError если строка не может быть прочитана из устройства
        :exception PermissionError если устройство не открыто на чтение
        """
        if not self.is_readable_device():
            raise PermissionError('Reading from the devices not allowed.')

        return self._take_line(self.__data)

    @staticmethod
    def _take_line(collection: List[str]) -> str:
        return collection.pop(0)


class NamedDevice(Device):
    def __init__(self, name: str, mode=DeviceMode.ReadOnly, data=None):
        super().__init__(mode, data)
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name


if __name__ == '__main__':
    device_0 = Device.open_device('/devices/dev0')
