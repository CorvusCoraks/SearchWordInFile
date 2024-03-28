""" Модуль визуализации с помощью PySide6. """
from typing import Callable, Optional
from PySide6.QtWidgets import QApplication, QPushButton, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt, Slot, Signal, QTimer, QPoint, QRect
from PySide6.QtGui import QGuiApplication
from Legacy.view_sig import ChildThread, Worker, Signals, SignalType
from Legacy.config import OUTPUT_LABEL_LENGTH
from protocol import AView
import sys
from queues import AbstractQueuesPull, QueueProtocol
# from config import ResultDict, OUTPUT_STRING


# class ViewMeta(type(QMainWindow), type(AView)):
#     pass


class PySyde6QMainWindow(QMainWindow):
    """ Класс GUI-окна приложения. """

    # Сигнал из дополнительной нити.
    signal_SearchResult = Signal(Signals)

    def __init__(self, app: QApplication):
        # С методом super() выдаёт ошибку
        # RuntimeError: '__init__' method of object's base class (PySyde6QMainWindow) not called.
        QMainWindow.__init__(self, flags=Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)



        # Окно уже ставилось в начальную позицию?
        self.__is_set_start_pos: bool = False
        # Счётчик, с помощью которого пропускается первое событие перемещения окна.
        # Если счётчик == 0, то первое перемещение уже было.
        self.__move_event_counter: int = 1

        self.__labels: list[QLabel] = []

        self.__app = app
        # https://stackoverflow.com/questions/74418142/minimal-pyside6-code-to-get-screen-resolution
        self.__screen_width, self.__screen_height = self.__app.primaryScreen().size().toTuple()
        print(self.__screen_width, self.__screen_height)

        # Объект живущий во вспомогательной нити и обрабатывающий сообщения.
        self.__worker: Worker = Worker(self.signal_SearchResult)

        self.setWindowTitle("PySide6 Application")

        # Метка подробностей о позиции, на которую был отклик.
        # self.lbl = QLabel("Hello World!")
        # Кнопка команды на начало поиска.
        self.btn = QPushButton("What to do.")

        # Просто виджет для помещения в центральную позицию главного окна (в этот виджет впихивается Layout)
        self.qw = QWidget()
        # Установка виджета в центральную част окна.
        self.setCentralWidget(self.qw)

        self.__layout = QVBoxLayout(self.qw)
        self.__layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__layout.addWidget(self.btn)
        # self.__layout.addWidget(self.lbl)

        # Связывание со слотом сигнала из вспомогательной нити о результатах поиска.
        self.signal_SearchResult.connect(self.__searchResult)
        # Подключение обработчика клика по кнопке
        self.btn.clicked.connect(self.__buttonClick)

        self.resize(200, 250)

        # print(self.frameSize(), self.maximumSize(), self.minimumSizeHint(), self.pos(), self.rect(), self.size(), sep='\n')
        # print(self.x(), self.y())

        # https://stackoverflow.com/questions/53234360/how-to-get-the-screen-position-of-qmainwindow-and-print-it
        # self.move(1360, 810)
        # print(self.mapToGlobal(QPoint(0, 0)))

        # width, height = QGuiApplication().primaryScreen().size().toTuple()
        # print(width, height)

        # Генерация "второго" (или нулевого?) фиктивного перемещения окна для обновления геометр. параметров окна.
        # self.move(0, 0)
        # self.move(0, 0)




    def moveEvent(self, e):
        # Установка первоначальной позиции окна на главном экране
        # Мистика в том, что при первом вызове методов возвращающих положение и размеры окна выходят ложные цифры.
        # Эти цифры обновляются только ПОСЛЕ первого обновления окна
        # (в данном случае, после второго (?) почему-то события перемещения)
        # https://stackoverflow.com/questions/53234360/how-to-get-the-screen-position-of-qmainwindow-and-print-it
        # Да и вообще, первое перемещение делат ОС, в центр экрана, так как окно изначально создаётся
        # в верхнем левом углу.
        # Что характерно, в приложении эти перемещения не инициируются, это, видимо, работа OC?
        if not self.__is_set_start_pos and self.__move_event_counter == 0:
            self.__is_set_start_pos = True
            # self.resize(self.width(), self.height() * 2)
            x = self.__screen_width - self.frameSize().width() - 10
            y = self.__screen_height - self.frameSize().height() - 10
            # Перемещаем окно в нужную позицию
            self.move(x, y)

        self.__move_event_counter = 0

        # print(self.pos())
        print(self.frameSize(), self.frameGeometry().size(), self.pos(), self.rect(), self.size(), sep='\n')
        print(self.x(), self.y())

        super(PySyde6QMainWindow, self).moveEvent(e)

    # def resizeEvent(self, event):
    #     super(PySyde6QMainWindow, self).resizeEvent(event)

    @Slot(Signals)
    def __searchResult(self, value):
        """ Обработчик сигнала о результатах поиска. """
        match value.signal:
            case SignalType.FOUNDED:
                for label in self.__labels:
                    self.__layout.removeWidget(label)
                    label.deleteLater()
                self.__labels = []
                # print("GUI reaction: ", SignalType.FOUNDED, '\n', value.content)
                # print(f"GUI reaction: {SignalType.FOUNDED} \n {value.content.result[1][0][:5:]}...")
                # self.lbl.setText(f"{value.content.result[1][0][:15:]}... {value.content.result[1][1][:15:]}...")
                for i in range(1, len(value.content.result)):
                    l_name = QLabel(f"{value.content.result[i][0][:OUTPUT_LABEL_LENGTH:]}...")
                    l_vacancy = QLabel(f"{value.content.result[i][1][:OUTPUT_LABEL_LENGTH:]}...")
                    self.__layout.addWidget(l_name)
                    self.__layout.addWidget(l_vacancy)
                    self.__labels.append(l_name)
                    self.__labels.append(l_vacancy)
                # self.repaint()
            case SignalType.NOT_FOUNDED:
                pass
            case _:
                print("Unknown search signal to GUI.")

    @Slot()
    def __buttonClick(self):
        """ Обработчик нажатия кнопки в GUI. """
        # Отправка сигнала в дополнительную нить.
        self.__worker.signalStartSearch_FromMainToWorker.emit(Signals(signal=SignalType.START_SEARCH))

        print(self.frameSize(), self.maximumSize(), self.minimumSizeHint(), self.pos(), self.rect(), self.size(), sep='\n')
        print(self.x(), self.y())

    @property
    def worker(self) -> Worker:
        return self.__worker


# Унаследовать сразу от QMainWindow и AView не получается: конфликт метаклассов.
# https://stackoverflow.com/questions/28720217/multiple-inheritance-metaclass-conflict
# http://www.phyast.pitt.edu/~micheles/python/metatype.html
class PySide6Realisation(AView):
    """ Класс визуализации на основе PySide6. """
    @Slot()
    def slotTimer(self):
        """ тестовый таймер для пингования дополнительной нити. """
        if self.__max_timer_count > 0:
            self.__window.worker.signalTimer_FromMainToWorker.emit("Hello from Timer from main thread!")
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
        # self.__worker = Worker()
        # Подсоединение сигнала, отправляемого в дополнительную нить
        # self.signal_buttonClick.connect(self.__worker.slotStartSearchHandler)
        # self.__worker.signalStartSearch_FromMainToWorker.connect(self.__worker.slotStartSearchHandler)

        # You need one (and only one) QApplication instance per application.
        # Pass in sys.argv to allow command line arguments for your app.
        # If you know you won't use command line arguments QApplication([]) works too.
        self.__app = QApplication(sys.argv)

        # width, height = self.__app.primaryScreen().size().toTuple()
        # print(width, height)

        # Create a Qt widget, which will be our window.
        self.__window = PySyde6QMainWindow(self.__app)

        # self.__window.setWindowTitle("PySide6 Application")
        # self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.BypassWindowManagerHint)
        # self.setWindowTitle("PySide6 Application")


        # Подключение обработчика клика по кнопке
        # btn.clicked.connect(self.__buttonClick)
        # btn.setMinimumSize()

        # self.__window.setCentralWidget(btn)
        # self.__window.setCentralWidget(btn)

        # Создание дочерней нити для обработки межблоковых сообщений.
        child_thread = ChildThread(self.__window.worker.run, queues_pull)

        # Отправка объекта в дополнительную нить на работу.
        self.__window.worker.moveToThread(child_thread)

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
