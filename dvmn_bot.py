import requests
import telegram
from urllib.parse import urljoin
from dotenv import load_dotenv
import os


def get_timestamp(data, bot, user_chat_id):
    if data['status'] == 'found':
        timestamp = data['last_attempt_timestamp']
        bot_send_message(data, bot, user_chat_id)
    if data['status'] == 'timeout':
        timestamp = data['timestamp_to_request']

    return timestamp


def bot_send_message(data, bot, user_chat_id):
    lesson_title = data['new_attempts'][0]['lesson_title']
    lesson_url = urljoin('https://dvmn.org', data['new_attempts'][0]['lesson_url'])
    if data['new_attempts'][0]['is_negative']:
        teacher_decision = f'У вас проверили работу "{lesson_title}"\n{lesson_url}\nК сожалению, в работе нашлись ошибки'
    else:
        teacher_decision = f'У вас проверили работу "{lesson_title}"\n{lesson_url}\nПреподавателю все понравилось, можно приступить к следующему уроку!'

    bot.send_message(chat_id=user_chat_id, text=teacher_decision)


if __name__ == '__main__':
    load_dotenv()
    dvmn_token = os.getenv('DVMN_TOKEN')
    dvmn_bot_token = os.getenv('DVMN_BOT_TOKEN')
    user_chat_id = os.getenv('USER_CHAT_ID')
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    bot = telegram.Bot(token=dvmn_bot_token)
    timestamp = None
    while True:
        try:
            response = requests.get(url, headers=headers, params={'timestamp': timestamp}, timeout=10)
            response.raise_for_status()
        except requests.ReadTimeout:
            pass
        except requests.ConnectionError:
            pass
        else:
            data = response.json()
            timestamp = get_timestamp(data, bot, user_chat_id)
