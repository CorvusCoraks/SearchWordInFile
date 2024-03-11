import protocol as p
from Legacy.view import PySide6Realisation
from Legacy.data import Data
from Legacy.wanted import WantedString
from Legacy.seeker import Seeker
from abstractyarn import AbstractQueuesPull, APP_FIN_QUEUE_NAME
import asyncio
from config import DATA_WAITING


class Logic:
    data: p.PSourceData = Data()
    wanted: p.PWanted = WantedString()
    seeker: p.PSeeker = Seeker()
    view: p.AView = PySide6Realisation()

    @classmethod
    def seek_trigger(cls) -> None:
        pass

    @classmethod
    def run_in_main(cls):
        cls.view.set_seek_method(cls.seek_trigger)

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
            if queues.incoming_waiting('find_it', DATA_WAITING):
                pass
            else:
                if queues.is_app_fin():
                    break
