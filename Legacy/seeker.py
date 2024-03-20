from protocol import PSeeker, PWanted, PSourceData
from config import NOT_STRING


class Seeker(PSeeker):
    def seek(self, wanted: PWanted, data: PSourceData) -> bool:
        string_for_search = wanted.get_wanted()
        if string_for_search == NOT_STRING:
            # todo обработать, если в буфере обмена не строка
            return False
        elif data.get_source_data.find(wanted.get_wanted()) > 0:
            return True
        else:
            return False
