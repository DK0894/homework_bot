import json


class WrongRequestToAPI(Exception):
    """Не удалось выполнить запрос к API Практикум.Домашка."""
    def __init__(self, message):
        super().__init__(message)
