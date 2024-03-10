from threading import Thread
from typing import Protocol, Any
from abc import ABC, abstractmethod
from enum import Enum
from queue import Queue
import asyncio
from dataclasses import dataclass


APP_FIN_QUEUE_NAME: str = 'app_fin'
ASYNCIO_SLEEP_TIME = 1000


class Direction(Enum):
    """ Направление очереди.
    Можно использовать для контроля правильности выбора очереди при отправке и получении данных."""
    TO_THREAD = 1
    FROM_THREAD = 2


@dataclass
class OneQueue:
    """ Очередь, содержащаяся в пуле очередей. """
    direction: Direction
    queue: Queue
    datatype: type


class PQueue(Protocol):
    """ Протокол отправки/получения данных в/из очереди. """
    @abstractmethod
    def send(self, queue_name: str, data: Any) -> None:
        """ Отправляет данные в очередь.

        :param queue_name: Имя очереди.
        :param data: Данные для отправки.
        :return:
        """
        ...

    @abstractmethod
    def receive(self, queue_name: str) -> Any:
        """ Получение данных из очереди.

        :param queue_name: Имя очереди.
        :return: Данные в очереди.
        """
        ...


class AQueuePull(ABC, PQueue):
    """ Пул очередей по обмену данными между основной нитью и дополнительной. """
    @abstractmethod
    def add_queue(self, queue_name: str, direction: Direction, datatype: type) -> None:
        """ Добавить очереди в пул очередей.

        :param queue_name: Имя очереди.
        :param direction: Направление очереди.
        :param datatype: Тип данных передаваемых в очереди.
        :return:
        """
        ...

    @abstractmethod
    def get_queue(self, queue_name: str) -> tuple[Queue, Direction, type]:
        """ Получить очередь по её имени.

        :param queue_name: Имя очереди.
        :return: Очередь.
        """
        ...

    async def incoming_waiting(self, queue_name: str) -> bool:
        """ Метод ожидания появления данных в очереди. А на фига он нужен? """
        while True:
            fin_queue, _, _ = self.get_queue(APP_FIN_QUEUE_NAME)
            if not fin_queue.empty():
                # Появилась команда на завершение приложения. Выходим из вечного цикла.
                break
            else:
                listened_queue, _, _ = self.get_queue(queue_name)
                if listened_queue.empty():
                    await asyncio.sleep(ASYNCIO_SLEEP_TIME)
                else:
                    return True


class AYarn(Thread, ABC):
    """ Класс дополнительной нити. """
    def __init__(self, queues: AQueuePull):
        super().__init__(daemon=True)

        self._queues: AQueuePull = queues

    @property
    def queues(self):
        """ Пул очередей по обмену данными. """
        return self._queues

    @abstractmethod
    async def async_run(self):
        """ Метод реализации асинхронности. """
        ...

    def run(self):
        asyncio.run(self.async_run())
