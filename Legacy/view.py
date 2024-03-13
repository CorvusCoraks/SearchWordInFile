from typing import Callable
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QMainWindow, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QThread, Signal, Slot
from protocol import AView
import sys
from queues import AbstractQueuesPull

# https://ruclient.ru/kak-peredat-znacenie-signala-mezdu-glavnym-i-docernim-potokami-v-pyside2-qthread/
# https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html#signals-and-slots
class ChildThread(QThread):

    # todo атрибут уровня класса
    signal_to_main: Signal = Signal(int)

    def __init__(self, queues_pull: AbstractQueuesPull):
        super().__init__()
        self._queues_pull = queues_pull
        # self.signal_success_finded: Signal = Signal(int)

    def run(self):
        # Ваша логика дочернего потока
        # Пример получения значения сигнала из главного потока
        value = self.get_value_from_main_thread()
        # Пример отправки значения сигнала в главный поток
        self.send_value_to_main_thread(value)
        print('ViewThread2')

        # todo атрибут уровня экземпляра класса. Как так? С какой целью?
        # Но если его объявлять не методом класса, то выдаст ошибку.
        self.signal_to_main.emit(42)

    def get_value_from_main_thread(self):

        # Получение значения сигнала из главного потока
        pass

    def send_value_to_main_thread(self, value):

        # Отправка значения сигнала в главный поток
        pass
        

class PySide6Realisation(AView):
    def __init__(self, queues_pull: AbstractQueuesPull):
        self._queues_pull = queues_pull

        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        self.__app = QApplication(sys.argv)

        # Create a Qt widget, which will be our window.
        # self.__window = QWidget()
        # self.__window = QPushButton("Push me!")
        self.__window = QMainWindow(flags=Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)
        self.__window.setWindowTitle("PySide6 Application")

        lbl = QLabel("Hello World!")
        btn = QPushButton("What to do.")
        # btn.setMinimumSize()

        self.__window.setCentralWidget(btn)

        child_thread = ChildThread(queues_pull)

        child_thread.signal_to_main.connect(self.handle_signal)

        child_thread.start()

        # box = QVBoxLayout()
        # box.addWidget(lbl)
        # box.addWidget(btn)
        #
        # self.__window.setLayout(box)

    @Slot(int)
    def handle_signal(self, value):
        # Обработка значений сигнала из дочернего потока
        print("Received signal value:", value)

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
