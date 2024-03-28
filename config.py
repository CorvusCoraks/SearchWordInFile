# Время в миллисекундах
msec = int

# Время в секундах
sec = float

# Время сна, между запросами наличия данных в очереди, sec
ASYNCIO_SLEEP_TIME: sec = 1

# Предельное время ожидания сообщения очереди, sec
DATA_WAITING: sec = 10

SOURCE_FILE_NAME: str = r"E:\Users\GreMal\Documents\Резюме\Вакансии с BSD-откликом.txt"

NOT_STRING: str = ''

# Результаты поиска.
# Каждый подсписок состоит из двух элементов: ключевая строка, должность.
# В первом подсписке сама разыскиваемая строка.
# [
# [Поисковая строка, SEARCHED_STRING_MARK],
# [Ключ, должность],
# [Ключ, должность],
# ...
# ]
ResultDict = list[list[str]]

SEARCHED_STRING_MARK = 'SEARCHED_STRING_MARK'



# OUTPUT_STRING: str = r"{name:15}{vacancy:15}"

# def to_msec(s: sec) -> msec:
#     return msec(s * 1000)
#
#
# def to_sec(ms: msec) -> sec:
#     return ms / 1000
