""" Модуль данных, в которых производится поиск. """
from protocol import PSourceData
from config import SOURCE_FILE_NAME


class Data(PSourceData):
    # def __init__(self):
    #     with open(SOURCE_FILE_NAME, encoding='UTF-8') as fn:
    #         self._data = fn.read()

    @property
    def get_source_data(self) -> str:
        # Чтение содержимого файла
        with open(SOURCE_FILE_NAME, encoding='UTF-8') as fn:
            data = fn.read()
        return data
