from protocol import PWanted
import pyperclip as p
from typing import Callable
import asyncio
from config import ASYNCIO_SLEEP_TIME
from time import sleep


class WantedString(PWanted):
    def __init__(self):
        self._uppercase: bool = True
        self._selected: str = None
        self._autoseek_trigger: Callable = None
        self._previous_text: str = ""
        p.copy(self._previous_text)

    def wanted(self) -> str:
        while self._previous_text == p.paste():
            # Цикл ожидания новых данных в буфере обмена.
            sleep(ASYNCIO_SLEEP_TIME)
        self._previous_text = p.paste()
        return self._previous_text

    def set_autoseek_trigger(self, seek_trigger: Callable) -> None:
        pass
