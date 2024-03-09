from typing import Callable
from PySide6 import QtGui
from protocol import AView


class PySide6Realisation(AView):
    def run_in_main(self) -> None:
        pass

    def set_seek_method(self, seek_trigger: Callable) -> None:
        pass

    def seeker_notification(self, success: bool) -> None:
        pass