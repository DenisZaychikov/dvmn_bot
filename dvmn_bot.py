import requests
import telegram
from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import time
import logging


class TgLogHandler(logging.Handler):

    def __init__(self, tg_bot, tg_user_chat_id):
        super().__init__()
        self.tg_bot = tg_bot
        self.tg_user_chat_id = tg_user_chat_id

    def emit(self, record):
        msg_to_bot = self.format(record)
        self.tg_bot.send_message(chat_id=tg_user_chat_id,
                                 text=msg_to_bot)


def send_message(data, bot, tg_user_chat_id):
    new_attempt = data['new_attempts'][0]
    lesson_title = new_attempt['lesson_title']
    lesson_url = urljoin('https://dvmn.org', new_attempt['lesson_url'])
    if new_attempt['is_negative']:
        teacher_decision = f'У вас проверили работу "{lesson_title}"\n{lesson_url}\nК сожалению, в работе нашлись ошибки'
    else:
        teacher_decision = f'У вас проверили работу "{lesson_title}"\n{lesson_url}\nПреподавателю все понравилось, можно приступить к следующему уроку!'

    bot.send_message(chat_id=tg_user_chat_id, text=teacher_decision)


if __name__ == '__main__':
    load_dotenv()
    dvmn_token = os.environ['DVMN_TOKEN']
    tg_bot_token = os.environ['TG_BOT_TOKEN']
    tg_user_chat_id = os.environ['TG_USER_CHAT_ID']
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    bot = telegram.Bot(token=tg_bot_token)

    logger = logging.getLogger()
    handler = TgLogHandler(bot, tg_user_chat_id)
    logger.addHandler(handler)

    timestamp = None
    while True:
        try:
            response = requests.get(url, headers=headers,
                                    params={'timestamp': timestamp},
                                    timeout=100)
            response.raise_for_status()
        except (
                requests.exceptions.ReadTimeout,
                requests.exceptions.HTTPError,
                requests.exceptions.ConnectionError
        ) as err:
            logger.error(err, exc_info=True)
            time.sleep(20)
        else:
            data = response.json()
            if data['status'] == 'found':
                timestamp = data['last_attempt_timestamp']
                send_message(data, bot, tg_user_chat_id)
            if data['status'] == 'timeout':
                timestamp = data['timestamp_to_request']
