import protocol as p
from Legacy.view import PySide6Realisation
from Legacy.data import Data
from Legacy.wanted import WantedString
from Legacy.seeker import Seeker
from queues import AbstractQueuesPull, Direction, Abonents, QueueName, QueueProtocol
from ryarn import QueuesPull
from time import sleep
from config import ASYNCIO_SLEEP_TIME


class Logic:
    queues_pull: AbstractQueuesPull = QueuesPull()

    data: p.PSourceData = Data()
    wanted: p.PWanted = WantedString()
    seeker: p.PSeeker = Seeker()
    view: p.AView = PySide6Realisation(queues_pull)

    @classmethod
    def seek_trigger(cls) -> None:
        """ Метод-триггер, запускающий поиск по сигналу из блока визуализации. """
        pass

    @classmethod
    def run_in_main(cls):
        cls.view.set_seek_method(cls.seek_trigger)

        # Настройка очередей.
        cls.queues_pull.add_queue(QueueName.WORD_SELECTED, Direction(Abonents.SEEKER, Abonents.VIEW), str)
        cls.queues_pull.add_queue(QueueName.APP_FIN, Direction(Abonents.VIEW, Abonents.SEEKER), bool)
        cls.queues_pull.add_queue(QueueName.FIND_IT, Direction(Abonents.VIEW, Abonents.SEEKER), str)
        cls.queues_pull.add_queue(QueueName.SEARCH_RESULT, Direction(Abonents.SEEKER, Abonents.VIEW), bool)

    @classmethod
    def seek_thread_method(cls, queues: QueueProtocol):
        """ Метод для исполнения в отдельной нити. """

        while True:
            # Цикл ожидания команды на поиск из GUI
            # Проверка на наличие команды на завершение приложения.
            if queues.is_app_fin(): break

            # queue, _, _ = queues.get_queue(QueueName.FIND_IT)
            # if not queue.empty():
            if not queues.is_empty(QueueName.FIND_IT):
                # В очереди есть команда на поиск
                # Извлечение команды
                queues.receive(QueueName.FIND_IT)

                # Результат поиска
                search_result = cls.seeker.seek(cls.wanted, cls.data)
                # Отправка результата в GUI
                queues.send(QueueName.SEARCH_RESULT, search_result)

            sleep(ASYNCIO_SLEEP_TIME)

        # while True:
        #     # Цикл ожидание изменений в буфере обмена - получение команды на поиск - команда на поиск - поиск
        #     # Получить новую строку для поиска
        #     search_string = Logic.wanted.wanted()
        #     # Отправить строку в блок визуализации
        #     queues.send('selected', search_string)
        #     # Ожидание команды на поиск.
        #     # Logic.data.get_source_data()
        #     print(Logic.seeker.seek(search_string, Logic.data))
        #     # if queues.incoming_waiting('find_it', DATA_WAITING):
        #     #     pass
        #     # else:
        #     #     if queues.is_app_fin():
        #     #         break
