import requests
import telegram
from urllib.parse import urljoin
from dotenv import load_dotenv
import os
import time


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
    # dvmn_token = os.getenv('DVMN_TOKEN')
    # dvmn_bot_token = os.getenv('DVMN_BOT_TOKEN')
    # tg_user_chat_id = os.getenv('TG_USER_CHAT_ID')
    dvmn_token = os.environ['DVMN_TOKEN']
    dvmn_bot_token = os.environ['DVMN_BOT_TOKEN']
    tg_user_chat_id = os.environ['TG_USER_CHAT_ID']
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_token}'}
    bot = telegram.Bot(token=dvmn_bot_token)
    timestamp = None
    while True:
        try:
            response = requests.get(url, headers=headers, params={'timestamp': timestamp}, timeout=100)
            response.raise_for_status()
        except requests.ReadTimeout:
            pass
        except requests.ConnectionError:
            print('Connection ERROR! Please, wait for 60sec, we will try to connect again!')
            time.sleep(60)
        else:
            data = response.json()
            if data['status'] == 'found':
                timestamp = data['last_attempt_timestamp']
                send_message(data, bot, tg_user_chat_id)
            if data['status'] == 'timeout':
                timestamp = data['timestamp_to_request']
