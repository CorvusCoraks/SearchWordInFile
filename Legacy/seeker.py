from protocol import PSeeker, PWanted, PSourceData
from config import NOT_STRING, ResultDict
from re import findall, MULTILINE
from queues import SearchResult


class Seeker(PSeeker):
    def _preparing(self, word: str):
        """ Подготовка разыскиваемой строки

        :param word: Разыскиваемая строка.
        :return: Подготовленная разыскиваемая строка.
        """
        # Экранирование точек в строке.
        result: str = word.replace('.', r'\.')
        return result

    # def seek(self, wanted: PWanted, data: PSourceData) -> bool:
    #     # Поиск по названию организации.
    #     # Формат:
    #     # Одна или несколько табуляций, Название организации (могут быть несколько слов с пробелами),
    #     # (Одна или несколько табуляций) или пробел. Подробности о позиции.
    #
    #     # string_for_search = wanted.get_wanted()
    #     #
    #     # if string_for_search == NOT_STRING:
    #     #     # todo обработать, если в буфере обмена не строка
    #     #     return False
    #     # else:
    #     #     string_for_search = self._preparing(string_for_search)
    #     #     # pattern = r'\t+.*?' + string_for_search + r'.*?\t+.*?\r\n'
    #     #     pattern = r'\t+.*?' + string_for_search + r'.*?\t+'
    #     #     pattern = r'^\t+.*?' + string_for_search + r'.*?\t+.+$'
    #     #     result = findall(pattern, data.get_source_data, flags=MULTILINE)
    #
    #     result = self._seek_inner(wanted, data)
    #
    #     if len(result) > 0:
    #         return True
    #     else:
    #         return False

    def seek(self, wanted: PWanted, data: PSourceData) -> ResultDict:
        # Поиск по названию организации.
        # Формат:
        # Одна или несколько табуляций, Название организации (могут быть несколько слов с пробелами),
        # (Одна или несколько табуляций) или пробел. Подробности о позиции.

        string_for_search = wanted.get_wanted()

        if string_for_search == NOT_STRING:
            # todo обработать, если в буфере обмена не строка
            return {}
        else:
            string_for_search = self._preparing(string_for_search)
            # pattern = r'\t+.*?' + string_for_search + r'.*?\t+.*?\r\n'
            pattern = r'\t+(.*?' + string_for_search + r'.*?)\t+'
            pattern = r'^\t+(.*?' + string_for_search + r'.*?)\t+(.+)$'

            search_result: list = findall(pattern, data.get_source_data, flags=MULTILINE)

            result = {value[0]: value[1] for value in search_result}

            return result

    def seek_old(self, wanted: PWanted, data: PSourceData) -> bool:
        string_for_search = wanted.get_wanted()
        if string_for_search == NOT_STRING:
            # todo обработать, если в буфере обмена не строка
            return False
        elif data.get_source_data.find(wanted.get_wanted()) > 0:
            return True
        else:
            return False
