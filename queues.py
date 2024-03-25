from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum
from queue import Queue
from typing import Protocol, Any, Optional, TypeVar, Union
from config import ResultDict


class Abonents(Enum):
    """ Абоненты отправки и получения сообщений через очереди. """
    SEEKER = 1
    VIEW = 2



@dataclass
class SearchResult:
    """ Результат поиска. """
    status: bool        # Успешно / неудачно.
    #request: str       # Что, собственно, искалось.
    result: ResultDict  # Список результатов.


# Типы данных для передачи через очереди.
# QueueData = TypeVar('QueueData', *[bool, str, SearchResult])

QueuesDataType = Union[bool, str, SearchResult]


@dataclass
class QueueName(ABC):
    """ Имена очередей приложения. Просто хранилище 'констант'. Создание экзепляров класса не предусмотрено. """

    # todo WORD_SELECTED Использовать не представляется возможным?
    WORD_SELECTED: str = 'selected'     # Слово выделено.
    FIND_IT: str = 'find_it'            # Команда из GUI на поиск.
    APP_FIN: str = 'app_fin'            # Команда на завершение приложения.
    SEARCH_RESULT: str = 'result'       # Результаты поиска


@dataclass
class Direction:
    """ Направление передачи сообщения. """
    sender: Abonents
    receiver: Abonents


@dataclass
class QueueInPull:
    """ Очередь, содержащаяся в пуле очередей. """
    queue: Queue                        # Очередь для передачи данных
    datatype: type(QueuesDataType)      # Тип передаваемы данных
    direction: Direction                # Направление очереди (откуда - куда)


class QueueProtocol(Protocol):
    """ Протокол отправки/получения данных в/из очереди. """
    @abstractmethod
    def send(self, queue_name: str, data: QueuesDataType) -> None:
        """ Отправляет данные в очередь.

        :param queue_name: Имя очереди.
        :param data: Данные для отправки.
        :return:
        """
        ...

    @abstractmethod
    def receive(self, queue_name: str) -> QueuesDataType:
        """ Получение данных из очереди.

        :param queue_name: Имя очереди.
        :return: Данные в очереди.
        """
        ...

    @abstractmethod
    def is_empty(self, queue_name: str) -> bool:
        """ Очередь пуста?

        :param queue_name: Имя очереди.
        """
        ...

    @abstractmethod
    def is_app_fin(self) -> bool:
        """ В очередь отправлена команда на завершение приложения. """
        ...


class AbstractQueuesPull(ABC, QueueProtocol):
    """ Пул очередей по обмену данными между основной нитью и дополнительной. """
    @abstractmethod
    def add_queue(self, queue_name: str, direction: Direction, datatype: type(QueuesDataType)) -> None:
        """ Добавить очереди в пул очередей.

        :param queue_name: Имя очереди.
        :param direction: Направление очереди.
        :param datatype: Тип данных передаваемых в очереди.
        :return:
        """
        ...

    # @abstractmethod
    # def get_queue(self, queue_name: str) -> tuple[Queue, Direction, type]:
    #     """ Получить очередь по её имени.
    #
    #     :param queue_name: Имя очереди.
    #     :return: Очередь.
    #     """
    #     ...



    # def incoming_waiting(self, queue_name: str, wating_time: int = None) -> bool:
    #     """ Метод ожидания появления данных в очереди. А на фига он нужен? """
    #     time = 0
    #     while True:
    #         if self.is_app_fin():
    #             # Появилась команда на завершение приложения. Выходим из вечного цикла.
    #             return False
    #         else:
    #             listened_queue, _, _ = self.get_queue(queue_name)
    #             if listened_queue.empty():
    #                 sleep(ASYNCIO_SLEEP_TIME)
    #                 if wating_time is not None and time > wating_time:
    #                     return False
    #                 else:
    #                     time += ASYNCIO_SLEEP_TIME
    #             else:
    #                 return True
