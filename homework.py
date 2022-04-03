import logging
import os
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv


load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 5
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


"""Настройка логгирования с отправкой сообщения об ошибке в чат telegram."""


# Переопределяю класс Handler для отправки сообщения в чат ботом.
# class TelegramBotHandler(logging.Handler):
#     def __init__(self, token, chat_id):
#         super().__init__()
#         self.token = token
#         self.chat_id = chat_id
#
#     def emit(self, record):
#         bot = telegram.Bot(self.token)
#         bot.send_message(self.chat_id, self.format(record))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        filename='project_log.log',
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    handler_stream = logging.StreamHandler()
    logger.addHandler(handler_stream)
    handler_file = logging.FileHandler(
        filename='bot_log_file', mode='w', encoding='UTF-8'
    )
    logger.addHandler(handler_file)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    )
    handler_file.setFormatter(formatter)
    # handler_chat = TelegramBotHandler(
    #     token=TELEGRAM_TOKEN, chat_id=TELEGRAM_CHAT_ID
    # )
    # handler_chat.setLevel(level=logging.ERROR)
    # logger.addHandler(handler_chat)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат."""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logger.info('Сообщение успешно отправлено')
    except telegram.TelegramError as error:
        logger.error(f'Сбой отправки сообщения: {error}')


def get_api_answer(current_timestamp):
    """Проверка доступности URL ENDPOINT."""
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    response = requests.get(
        ENDPOINT, headers=HEADERS, params=params
    )
    if response.status_code != HTTPStatus.OK:
        logger.error(
            f'URL {ENDPOINT} недоступен: {telegram.TelegramError.__name__}'
        )
        raise telegram.TelegramError(message=f'URL {ENDPOINT} недоступен')
    try:
        response.json()
    except NameError as error:
        logger.error(f'JSON сломан: {error}')
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    try:
        response['homeworks']
    except KeyError as error:
        logger.error(f'Получен некорректный ответ API: KeyError - {error}')
    try:
        response['homeworks'][0].get('homework_name')
    except telegram.TelegramError as error:
        logger.error(f'Отсутствуют данные о названии работы - {error}')
    return response['homeworks']


def parse_status(homework):
    """Извлекает из информации о домашней работе статус этой работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    try:
        HOMEWORK_STATUSES[homework_status]
    except KeyError as error:
        logger.error(f'Неизвестный статус домашней работы: KeyError - {error}')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    some_variables = {
            'PRACTICUM_TOKEN': PRACTICUM_TOKEN,
            'TELEGRAM_TOKEN': TELEGRAM_TOKEN,
            'TELEGRAM_CHAT_ID': TELEGRAM_CHAT_ID
        }
    for variable, exp in some_variables.items():
        if exp is None:
            logger.critical(f'Отсутствует переменная окружения: {variable}')
            return False
    return True


# def check_tokens():
#     """Проверка доступности переменных окружения."""
#     some_variables = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
#     for variable in some_variables:
#         if variable is not None:
#             return True
#     logger.critical(f'Отсутствует переменная окружения')
#     return False


def main():
    """Основная логика работы бота."""
    if not check_tokens():
        exit()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())
    message_error = None

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if 'status' in homeworks[0]:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            current_timestamp = response.get('current_date')

        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            if message_error != message:
                message_error = message
                send_message(bot, message)
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
