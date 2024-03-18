from PySide6.QtCore import QThread, Signal, QObject, QTimer, Slot
from queues import AbstractQueuesPull
from enum import Enum
from typing import Callable


# Пауза между тиками тикера нити.
TICKER_PAUSE = 1000


class Signals(Enum):
    START_SEARCH = 0
    NOT_FOUNDED = 1
    FOUNDED = 2


class ChildThread(QThread):
    """ Класс дополнительной нити GUI. """
    def __init__(self, to_thread_init_method: Callable, queues_pull: AbstractQueuesPull):
        super().__init__()

        to_thread_init_method()


class Worker(QObject):
    """ Класс, обеспечивающий возможность отправки сигналов в главную нить GUI (работает в дополнительной нити) """
    signalStartSearch_FromMainToWorker = Signal(Signals)
    signalTimer_FromMainToWorker = Signal(str)
    # signalTicker = Signal(int)

    # def __init__(self, searchResultSignal: Signal):
    #     super().__init__()
    #
    #     # Запуск этого сигнала из данного объекта (emit()) передаст результат поиска в нить GUI
    #     self.__searchResultSignal = searchResultSignal

    @Slot(Signals)
    def slotStartSearchHandler(self, value):
        """ Обработчик нажатия кнопки поиска в GUI. """
        match value:
            case Signals.START_SEARCH:
                print(f"Main Window signal: Start Search! Value from Main Window: {value}")
            case _:
                print("Unknown press button signal.")

    @Slot(str)
    def __slotTimer(self, value):
        print(f"From Main Window signal: {value}")

    @Slot()
    def __slotWorkerTicker(self):
        """ Метод, периодически запускаемый в нити по сигналу тикера. """
        print("Внутренний тикер дополнительной нити GUI.")

    def run(self):
        print("Run объекта.")
        self.signalStartSearch_FromMainToWorker.connect(self.slotStartSearchHandler)
        # Связь сигнала со слотом.
        self.signalTimer_FromMainToWorker.connect(self.__slotTimer)
        # ... Другая функциональность потока ...

        # Задание в нити тикера, по сигналу которого будут запускаться периодические функции.
        self.__workerTicker = QTimer()
        self.__workerTicker.timeout.connect(self.__slotWorkerTicker)
        self.__workerTicker.start(TICKER_PAUSE)



# # https://ruclient.ru/kak-peredat-znacenie-signala-mezdu-glavnym-i-docernim-potokami-v-pyside2-qthread/
# # https://doc.qt.io/qtforpython-6/tutorials/basictutorial/signals_and_slots.html#signals-and-slots
# class ChildThread(QThread):
#
#     # todo атрибут уровня класса
#     signal_to_main: Signal = Signal(int)
#     signal_start_search = Signal(int)
#
#     def __init__(self, queues_pull: AbstractQueuesPull):
#         super().__init__()
#
#         self._queues_pull = queues_pull
#         # self.signal_success_finded: Signal = Signal(int)
#
#     def run(self):
#         # self.exec()
#         # Ваша логика дочернего потока
#         # Пример получения значения сигнала из главного потока
#         value = self.get_value_from_main_thread()
#         # Пример отправки значения сигнала в главный поток
#         self.send_value_to_main_thread(value)
#         print('ViewThread2')
#
#         # todo атрибут уровня экземпляра класса. Как так? С какой целью?
#         # Но если его объявлять не методом класса, то выдаст ошибку.
#         self.signal_to_main.emit(42)
#
#     def get_value_from_main_thread(self):
#
#         # Получение значения сигнала из главного потока
#         pass
#
#     def send_value_to_main_thread(self, value):
#
#         # Отправка значения сигнала в главный поток
#         pass
