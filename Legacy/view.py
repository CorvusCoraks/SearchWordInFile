from typing import Callable
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow
from protocol import AView
import sys


class PySide6Realisation(AView):
    def __init__(self):
        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        self.__app = QApplication(sys.argv)

        # Create a Qt widget, which will be our window.
        # self.__window = QWidget()
        # self.__window = QPushButton("Push me!")
        self.__window = QMainWindow()

    def run_in_main(self) -> None:
        # Must be in this method. In __init__ do not show window. Why?
        self.__window.show()  # IMPORTANT!!!!! Windows are hidden by default.

        # Start the event loop.
        self.__app.exec()
        # Your application won't reach here until you exit and the event
        # loop has stopped.

    def set_seek_method(self, seek_trigger: Callable) -> None:
        pass

    def seeker_notification(self, success: bool) -> None:
        pass
