""" Модуль с протоколами, абстрактными классами и интерфейсами. """
from typing import Protocol, Any, Callable
from abc import ABC, abstractmethod
from queues import AbstractQueuesPull, QueueProtocol
from config import ResultDict


class PSourceData(Protocol):
    """ Данные, в которых необходимо произвести поиск. """
    @property
    @abstractmethod
    def get_source_data(self) -> str:
        """ Получение данных. """
        ...


class PWanted(Protocol):
    """ Данные, которые необходимо найти. """
    @abstractmethod
    def wanted(self) -> Any:
        """ Данные, которые необходимо найти. deprecated?"""
        ...

    @abstractmethod
    def get_wanted(self) -> str:
        """ Данные, которые необходимо найти. """
        ...

    @abstractmethod
    def set_autoseek_trigger(self, seek_trigger: Callable) -> None:
        """ Установка метода-триггера, запускающего поиск.

        :param seek_trigger: Метод-триггер, запускающий автоматический поиск, без участия пользователя.
        :return:
        """
        ...


class PSeeker(Protocol):
    """ Объект, производящий поиск. """
    @abstractmethod
    def seek(self, wanted: PWanted, data: PSourceData) -> ResultDict:
        """ Поиск данных.

        :param wanted: Данные, которые необходимо найти.
        :param data: Данные, в которых производится поиск.
        :return: Список результатов поиска.
        """
        ...


class AView(ABC):
    """ Класс отображения. """
    @abstractmethod
    def __init__(self, queues_pull: QueueProtocol):
        """

        :param queues_pull: Пул очередей обмена сообщениями между блоками приложения.
        """
        ...

    @abstractmethod
    def run_in_main(self) -> None:
        """ Метод, который, при необходимости, надо разместить в модуле main, для корректной работы визуализации. """
        ...

    @abstractmethod
    def set_seek_method(self, seek_trigger: Callable) -> None:
        """ Установка метода-триггера, запускающего поиск.

        :param seek_trigger: метод-триггер, запускающий поиск.
        :return:
        """
        ...

    @abstractmethod
    def seeker_notification(self, success: bool) -> None:
        """ Метод предназначенный для отправки в класс визуализации результата поиска.

        :param success: Поиск успешен? Или нет?
        :return:
        """
        ...
