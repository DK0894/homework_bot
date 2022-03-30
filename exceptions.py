class MassageNotSend(Exception):
    """Исключение при отправке сообщения."""
    pass


class EndpointNotAvailable(Exception):
    """Исключение при отсутствии доступа к API
    https://practicum.yandex.ru/api/user_api/homework_statuses.
    """
    pass


class MissingEnvironmentVariables(Exception):
    """Исключение отсутствия обязательных переменных окружения"""
    pass


class MissingExpectedAPIKeys(Exception):
    """Исключение отсутствия ожидаемых ключей в ответе API"""
    pass


class UnknownStatusAPI(Exception):
    """Исключение некоррекного статуса домашней работы в ответе API"""
    pass


# class NotResponseNewStatus(Exception):
#     """Исключение при отсутствии в ответе новых статусов"""
#     pass


class ServerError(Exception):
    """Исключение невозможности сервера обработать запрос"""
    pass
