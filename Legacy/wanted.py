""" Модуль определения поискового запроса. """
from protocol import PWanted
import pyperclip as p
from typing import Callable, Optional, Any
import asyncio
from config import ASYNCIO_SLEEP_TIME, NOT_STRING
from time import sleep


class WantedString(PWanted):
    def __init__(self):
        self._uppercase: bool = True
        self._selected: Optional[str] = None
        self._autoseek_trigger: Optional[Callable] = None
        self._previous_text: str = ""
        p.copy(self._previous_text)

    def wanted(self) -> str:
        while self._previous_text == p.paste():
            # Цикл ожидания новых данных в буфере обмена.
            sleep(ASYNCIO_SLEEP_TIME)
        self._previous_text = p.paste()
        return self._previous_text

    def get_wanted(self) -> str:
        """ Возвращает строку для поиска.

        :return: Если NOT_STRING, то в буфере обмена не строка.
        """
        may_be_string: Any = p.paste()
        if isinstance(may_be_string, str):
            return may_be_string
        # raise TypeError('An attempt to extract an object from the clipboard is not a string.')
        return NOT_STRING

    def set_autoseek_trigger(self, seek_trigger: Callable) -> None:
        pass
