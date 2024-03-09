from protocol import PWanted
import pyperclip as p
from typing import Callable


class WantedString(PWanted):
    def __init__(self):
        self._uppercase: bool = True
        self._selected: str = None
        self._autoseek_trigger: Callable = None

    def wanted(self) -> str:
        return "wanted_string"

    def set_autoseek_trigger(self, seek_trigger: Callable) -> None:
        pass
