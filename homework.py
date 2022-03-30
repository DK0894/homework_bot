import logging
import os
import time
from http import HTTPStatus

import requests
import telegram
from dotenv import load_dotenv

import exceptions

load_dotenv()


PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_TIME = 600
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}


HOMEWORK_STATUSES = {
    'approved': 'Работа проверена: ревьюеру всё понравилось. Ура!',
    'reviewing': 'Работа взята на проверку ревьюером.',
    'rejected': 'Работа проверена: у ревьюера есть замечания.'
}


"""Настройка логгирования."""
logging.basicConfig(
    level=logging.INFO,
    filename='project_log.log',
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)


def send_message(bot, message):
    """Отправляет сообщение в Telegram чат"""
    try:
        bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=message
        )
        logger.info('Сообщение успешно отправлено')
    except exceptions.MassageNotSend as error:
        logger.error(f'Сбой отправки сообщения: {error}')


def get_api_answer(current_timestamp):
    """Проверка доступности URL ENDPOINT."""
    timestamp = current_timestamp
    params = {'from_date': timestamp}
    response = requests.get(
        ENDPOINT, headers=HEADERS, params=params
    )
    try:
        response = requests.get(
            ENDPOINT, headers=HEADERS, params=params
        )
    except exceptions.EndpointNotAvailable as error:
        logger.error(
            f'Ошибка при запросе к API, ENDPOINT недоступен: {error}'
        )
    if response.status_code != HTTPStatus.OK:
        logger.error(exceptions.ServerError.__doc__)
        raise exceptions.ServerError
    return response.json()


def check_response(response):
    """Проверяет ответ API на корректность."""
    try:
        response['homeworks']
    except exceptions.MissingExpectedAPIKeys as error:
        logger.error(f'Получен некорректный ответ API: {error}')
    if 'homework_name' and 'status' not in response['homeworks'][0]:
        logger.error(exceptions.MissingExpectedAPIKeys.__doc__)
    return response['homeworks']


def parse_status(homework):
    """Извлекает из информации о домашней работе статус этой работы."""
    homework_name = homework.get('homework_name')
    homework_status = homework.get('status')
    try:
        homework_status in HOMEWORK_STATUSES
    except exceptions.UnknownStatusAPI as error:
        logger.error(f'Неизвестный статус домашней работы: {error}')
    verdict = HOMEWORK_STATUSES[homework_status]
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_tokens():
    """Проверка доступности переменных окружения."""
    some_variables = [PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID]
    for variable in some_variables:
        if variable is not None:
            return True
    logger.critical(f'Отсутствует переменная окружения')
    return False


def main():
    """Основная логика работы бота."""

    check_tokens()

    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())

    while True:
        try:
            response = get_api_answer(current_timestamp)
            homeworks = check_response(response)
            if 'status' in homeworks[0]:
                message = parse_status(homeworks[0])
                send_message(bot, message)
            current_timestamp = response.get('current_date')
            time.sleep(RETRY_TIME)

        except IndexError as error:
            message = f'Сбой в работе программы: {error}'
            message_error = str(message)
            if message != message_error:
                send_message(bot, message)
        time.sleep(RETRY_TIME)


if __name__ == '__main__':
    main()
