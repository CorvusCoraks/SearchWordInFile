import protocol as p
from Legacy.view import PySide6Realisation
from Legacy.data import Data
from Legacy.wanted import WantedString
from Legacy.seeker import Seeker
from queues import AbstractQueuesPull, APP_FIN_QUEUE_NAME, Direction, Abonents
from ryarn import QueuesPull


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
        cls.queues_pull.add_queue('selected', Direction(Abonents.SEEKER, Abonents.VIEW), str)
        cls.queues_pull.add_queue(APP_FIN_QUEUE_NAME, Direction(Abonents.VIEW, Abonents.SEEKER), bool)
        cls.queues_pull.add_queue('find_it', Direction(Abonents.VIEW, Abonents.SEEKER), str)

    @classmethod
    def seek_thread_method(cls, queues: AbstractQueuesPull):
        """ Метод для исполнения в отдельной нити. """
        while True:
            # Цикл ожидание изменений в буфере обмена - получение команды на поиск - команда на поиск - поиск
            # Получить новую строку для поиска
            search_string = Logic.wanted.wanted()
            # Отправить строку в блок визуализации
            queues.send('selected', search_string)
            # Ожидание команды на поиск.
            # Logic.data.get_source_data()
            print(Logic.seeker.seek(search_string, Logic.data))
            # if queues.incoming_waiting('find_it', DATA_WAITING):
            #     pass
            # else:
            #     if queues.is_app_fin():
            #         break
