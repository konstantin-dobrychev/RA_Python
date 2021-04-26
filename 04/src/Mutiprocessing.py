import time

from multiprocessing import Process, current_process


class Task(object):
    def __init__(self):
        self.__is_running = False

    @property
    def __pid(self):
        return current_process().pid

    @property
    def __process_name(self):
        return current_process().name

    def __call__(self, name: str):
        print(f'Task "{name}" started')
        self.__is_running = True

        while self.__is_running:
            print(f'{self.__process_name}. task: {name}, pid: {self.__pid}')
            time.sleep(1)

        print(f'Task "{name}" stopped')

    def cancel(self):
        self.__is_running = False


if __name__ == '__main__':
    tasks = [Task() for _ in range(4)]
    processes = [Process(target=task, args=(f'Task_{index}',)) for index, task in enumerate(tasks)]

    try:
        for process in processes:
            process.start()

        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for task in tasks:
            task.cancel()
