import cv2
import time
import sys

import numpy as np

from abc import abstractmethod

from PIL import ImageGrab


class AbstractFrameGenerator(object):
    def __init__(self, fps=25):
        self._fps = fps

    def __iter__(self):
        return self

    def __next__(self):
        time.sleep(1 / float(self._fps))
        success, data = self._generate_next_frame()

        if success:
            ret, jpeg = cv2.imencode('.jpg', data)
            return jpeg
        else:
            print("Can't read frame")
            sys.exit(1)

    @abstractmethod
    def _generate_next_frame(self) -> tuple:
        pass


class DesktopFrameGenerator(AbstractFrameGenerator):
    def __init__(self, box: tuple, fps=25):
        super().__init__(fps)
        self.__box = box

    def _generate_next_frame(self) -> tuple:
        return True, np.array(ImageGrab.grab(self.__box))


class CameraFrameGenerator(AbstractFrameGenerator):
    def __init__(self, fps=25):
        super().__init__(fps)
        self.__capture = cv2.VideoCapture(0)

    def _generate_next_frame(self) -> tuple:
        return self.__capture.read()


if __name__ == '__main__':
    frame_generator = DesktopFrameGenerator(box=(100, 10, 400, 780), fps=12)

    for index, frame in enumerate(frame_generator):
        with open('frames/frame_{0}.jpg'.format(index), 'wb') as f:
            f.write(frame)
