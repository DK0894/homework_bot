class WrongRequestToAPI(Exception):
    """Не удалось выполнить запрос к API Практикум.Домашка."""
    pass


class URLNotAvailable(Exception):
    """URL недоступено, код ответа сервера не 200."""
    pass


class NoHomeworkStatus(KeyError):
    """Отсутствуют данные о статусе домешней работы."""
    pass


class DataTypeNotCorrect(Exception):
    """Некорректный тип данных в JSON файле ответа API."""
    pass


class JSONInvalidCode(Exception):
    """Поломан полученный файл JSON."""
    pass


class KeywordStatusLost(Exception):
    """Отсутстувует ключевое слово 'status'"""
    pass
