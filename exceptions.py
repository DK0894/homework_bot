class WrongRequestToAPI(Exception):
    """Не удалось выполнить запрос к API Практикум.Домашка."""
    def __str__(self):
        return WrongRequestToAPI.__doc__


class URLNotAvailable(Exception):
    """URL недоступено, код ответа сервера не 200."""
    def __str__(self):
        return URLNotAvailable.__doc__


class NoHomeworkStatus(KeyError):
    """Отсутствуют данные о статусе домешней работы."""
    def __str__(self):
        return NoHomeworkStatus.__doc__
