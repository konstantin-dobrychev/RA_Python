import time

from multiprocessing import current_process
from threading import Thread, Lock, current_thread


class Task(object):
    def __init__(self):
        self.__is_running = False

    @property
    def __pid(self):
        return current_process().pid

    @property
    def __tid(self):
        return current_thread().native_id

    @property
    def __thread_name(self):
        return current_thread().name

    def __call__(self, name: str):
        print(f'Task "{name}" started')
        self.__is_running = True

        while self.__is_running:
            print(f'{self.__thread_name}. task: {name}, pid: {self.__pid}, tid: {self.__tid}')
            time.sleep(2)

        print(f'Task "{name}" stopped')

    def cancel(self):
        self.__is_running = False


if __name__ == '__main__':
    lock = Lock()
    tasks = [Task() for _ in range(4)]
    threads = [Thread(target=task, args=(f'Task_{index}',)) for index, task in enumerate(tasks)]

    try:
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        for task in tasks:
            task.cancel()
