from threading import Thread
from typing import Callable
from abc import ABC
from queues import AbstractQueuesPull, QueueProtocol


class AbstractYarn(Thread, ABC):
    """ Класс дополнительной нити. """
    # todo уже не абстрактный класс.
    def __init__(self, queues: QueueProtocol, in_thread_method: Callable):
        """

        :param queues: Пул очередей, для взаимодействия с нитью.
        :param in_thread_method: внешний метод, предназначенный для запуска внутри нити.
        """
        super().__init__(target=in_thread_method, daemon=True, args=(queues,))

        self._queues: QueueProtocol = queues
        # self._asyncio_method: Callable = asyncio_method_in_thread_execution
        self._in_thread_method: Callable = in_thread_method

    @property
    def queues(self):
        """ Пул очередей по обмену данными. """
        return self._queues
