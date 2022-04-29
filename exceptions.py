class WrongRequestToAPI(Exception):
    """Не удалось выполнить запрос к API Практикум.Домашка."""
    def __init__(self, massage):
        self.massage = massage


class URLNotAvailable(Exception):
    """URL недоступено, код ответа сервера не 200."""
    def __init__(self, massage):
        self.massage = massage


class NoHomeworkStatus(KeyError):
    """Отсутствуют данные о статусе домешней работы."""
    def __init__(self, massage):
        self.massage = massage


class DataTypeNotCorrect(Exception):
    """Некорректный тип данных в JSON файле ответа API."""
    def __init__(self, massage):
        self.massage = massage
