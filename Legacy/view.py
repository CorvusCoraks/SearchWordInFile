from typing import Callable
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel
from PySide6.QtCore import Qt, Slot, Signal, QTimer
from Legacy.view_sig import ChildThread, Worker, Signals
from protocol import AView
import sys
from queues import AbstractQueuesPull, QueueProtocol


# class ViewMeta(type(QMainWindow), type(AView)):
#     pass


class PySyde6QMainWindow(QMainWindow):
    """ Класс GUI-окна приложения. """

    # Сигнал из дополнительной нити.
    signal_SearchResult = Signal(Signals)

    def __init__(self, worker: Worker):
        """

        :param worker: объект, который работает в дополнительной нити.
        """

        # С методом super() выдаёт ошибку
        # RuntimeError: '__init__' method of object's base class (PySyde6QMainWindow) not called.
        QMainWindow.__init__(self, flags=Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)

        self.__worker = worker

        self.setWindowTitle("PySide6 Application")

        self.lbl = QLabel("Hello World!")
        self.btn = QPushButton("What to do.")

        self.setCentralWidget(self.btn)

        # Связывание со слотом сигнала из вспомогательной нити о результатах поиска.
        self.signal_SearchResult.connect(self.__searchResult)
        # Подключение обработчика клика по кнопке
        self.btn.clicked.connect(self.__buttonClick)

    @Slot(Signals)
    def __searchResult(self, value):
        """ Обработчик сигнала о результатах поиска. """
        match value:
            case Signals.FOUNDED:
                pass
            case Signals.NOT_FOUNDED:
                pass
            case _:
                print("Unknown search signal to GUI.")

    @Slot()
    def __buttonClick(self):
        """ Обработчик нажатия кнопки в GUI. """
        # Отправка сигнала в дополнительную нить.
        self.__worker.signalStartSearch_FromMainToWorker.emit(Signals.START_SEARCH)


# Унаследовать сразу от QMainWindow и AView не получается: конфликт метаклассов.
# https://stackoverflow.com/questions/28720217/multiple-inheritance-metaclass-conflict
# http://www.phyast.pitt.edu/~micheles/python/metatype.html
class PySide6Realisation(AView):
    """ Класс визуализации на основе PySide6. """
    @Slot()
    def slotTimer(self):
        """ тестовый таймер для пингования дополнительной нити. """
        if self.__max_timer_count > 0:
            self.__worker.signalTimer_FromMainToWorker.emit("Hello from Timer from main thread!")
            self.__max_timer_count -= 1
        else:
            if self.__tm.isActive():
                print("Timer stopped!")
                self.__tm.stop()

    def __init__(self, queues_pull: QueueProtocol):
        """

        :param queues_pull: Пул очередей для обмена сообщения с блоком поиска приложения.
        """
        # super().__init__()
        # QMainWindow.__init__(self, flags=Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)

        self._queues_pull = queues_pull

        self.__max_timer_count = 5

        # Объект живущий во вспомогательной нити и обрабатывающий сообщения.
        # self.__worker = Worker(self.signal_SearchResult)
        self.__worker = Worker()
        # Подсоединение сигнала, отправляемого в дополнительную нить
        # self.signal_buttonClick.connect(self.__worker.slotStartSearchHandler)
        # self.__worker.signalStartSearch_FromMainToWorker.connect(self.__worker.slotStartSearchHandler)

        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        self.__app = QApplication(sys.argv)

        # Create a Qt widget, which will be our window.
        self.__window = PySyde6QMainWindow(self.__worker)

        # self.__window.setWindowTitle("PySide6 Application")
        # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)
        # self.setWindowTitle("PySide6 Application")


        # Подключение обработчика клика по кнопке
        # btn.clicked.connect(self.__buttonClick)
        # btn.setMinimumSize()

        # self.__window.setCentralWidget(btn)
        # self.__window.setCentralWidget(btn)

        # Создание дочерней нити для обработки межблоковых сообщений.
        child_thread = ChildThread(self.__worker.run, queues_pull)

        # Отправка объекта в дополнительную нить на работу.
        self.__worker.moveToThread(child_thread)

        # Связь сигнала со слотом (обработчиком)
        # child_thread.signal_to_main.connect(self.handle_signal)

        # Запуск дочерней нити.
        child_thread.start()

        # box = QVBoxLayout()
        # box.addWidget(lbl)
        # box.addWidget(btn)
        #
        # self.__window.setLayout(box)

        self.__tm = QTimer()
        self.__tm.timeout.connect(self.slotTimer)
        self.__tm.start(1000)
        # self.__tm = self.__window.startTimer(1000)

    @Slot(int)
    def handle_signal(self, value):
        # Обработка значений сигнала из дочернего потока. Метод не используется?
        print("Received signal value:", value)

    def run_in_main(self) -> None:
        # Must be in this method. In __init__ do not show window. Why?
        # self.__window.show()  # IMPORTANT!!!!! Windows are hidden by default.
        self.__window.show()  # IMPORTANT!!!!! Windows are hidden by default.

        # Start the event loop.
        self.__app.exec()
        # Your application won't reach here until you exit and the event
        # loop has stopped.

    def set_seek_method(self, seek_trigger: Callable) -> None:
        pass

    def seeker_notification(self, success: bool) -> None:
        pass


# class PySide6Realisation(AView):
#     def __init__(self, queues_pull: AbstractQueuesPull):
#         self._queues_pull = queues_pull
#
#         # You need one (and only one) QApplication instance per application.
#         # Pass in sys.argv to allow command line arguments for your app.
#         # If you know you won't use command line arguments QApplication([]) works too.
#         self.__app = QApplication(sys.argv)
#
#         # Create a Qt widget, which will be our window.
#         self.__window = QMainWindow(flags=Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)
#         self.__window.setWindowTitle("PySide6 Application")
#
#         lbl = QLabel("Hello World!")
#         btn = QPushButton("What to do.")
#         # btn.setMinimumSize()
#
#         self.__window.setCentralWidget(btn)
#
#         # Создание дочерней нити для обработки межблоковых сообщений.
#         child_thread = ChildThread(queues_pull)
#
#         # Связь сигнала со слотом (обработчиком)
#         child_thread.signal_to_main.connect(self.handle_signal)
#
#         # Запуск дочерней нити.
#         child_thread.start()
#
#         # box = QVBoxLayout()
#         # box.addWidget(lbl)
#         # box.addWidget(btn)
#         #
#         # self.__window.setLayout(box)
#
#     @Slot(int)
#     def handle_signal(self, value):
#         # Обработка значений сигнала из дочернего потока
#         print("Received signal value:", value)
#
#     def run_in_main(self) -> None:
#         # Must be in this method. In __init__ do not show window. Why?
#         self.__window.show()  # IMPORTANT!!!!! Windows are hidden by default.
#
#         # Start the event loop.
#         self.__app.exec()
#         # Your application won't reach here until you exit and the event
#         # loop has stopped.
#
#     def set_seek_method(self, seek_trigger: Callable) -> None:
#         pass
#
#     def seeker_notification(self, success: bool) -> None:
#         pass
