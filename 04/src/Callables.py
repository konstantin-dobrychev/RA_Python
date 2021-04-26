from typing import Callable, Iterable, List


def debug(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print(f'Call: {func} with {len(args) + len(kwargs)} args')
        return func(*args, **kwargs)

    return wrapper


def _sum(a: float, b: float) -> float:
    return a + b


def plus(x: float) -> Callable[[float], float]:
    return lambda y: _sum(x, y)


class Sum(object):
    def __init__(self):
        self.__calls_history = []

    @property
    def calls_history(self) -> List[str]:
        return self.__calls_history

    def __call__(self, a: float, b: float) -> float:
        result = a + b

        self.__calls_history.append(f'{a} + {b} = {result}')

        return result


class Sqr(object):
    def __init__(self):
        self.__calls_history = []

    @property
    def calls_history(self) -> List[str]:
        return self.__calls_history

    def __call__(self, x: float) -> float:
        result = x ** 2

        self.__calls_history.append(f'{x} ** 2 = {result}')

        return result


def for_each(iterable: Iterable, func: Callable) -> Callable:
    for value in iterable:
        func(value)

    return func


if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]

    print(for_each(numbers, plus(10)))
    print(numbers)

    for_each(numbers, print)
    for_each(numbers, lambda x: print(x ** x))

    sqr_func: Sqr = for_each(numbers, Sqr())
    print(sqr_func.calls_history)
