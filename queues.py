from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from time import sleep
from typing import Protocol, Any
from config import ASYNCIO_SLEEP_TIME


APP_FIN_QUEUE_NAME: str = 'app_fin'


class Abonents(Enum):
    """ Абоненты отправки и получения сообщений через очереди. """
    SEEKER = 1
    VIEW = 2


@dataclass
class Direction:
    """ Направление передачи сообщения. """
    sender: Abonents
    receiver: Abonents


@dataclass
class QueueInPull:
    """ Очередь, содержащаяся в пуле очередей. """
    queue: Queue
    datatype: type
    direction: Direction


class QueueProtocol(Protocol):
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


class AbstractQueuesPull(ABC, QueueProtocol):
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

    def is_app_fin(self) -> bool:
        """ В очередь отправлена команда на завершение приложения. """
        fin_queue, _, _ = self.get_queue(APP_FIN_QUEUE_NAME)
        return not fin_queue.empty()

    def incoming_waiting(self, queue_name: str, wating_time: int = None) -> bool:
        """ Метод ожидания появления данных в очереди. А на фига он нужен? """
        time = 0
        while True:
            if self.is_app_fin():
                # Появилась команда на завершение приложения. Выходим из вечного цикла.
                return False
            else:
                listened_queue, _, _ = self.get_queue(queue_name)
                if listened_queue.empty():
                    sleep(ASYNCIO_SLEEP_TIME)
                    if wating_time is not None and time > wating_time:
                        return False
                    else:
                        time += ASYNCIO_SLEEP_TIME
                else:
                    return True
