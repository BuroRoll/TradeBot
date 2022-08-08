import os

import requests

telegram_api_token = os.getenv('TELEGRAM_API_TOKEN')
my_chat_id = os.getenv('MY_CHAT_ID')

api_url = f'https://api.telegram.org/bot{telegram_api_token}/sendMessage'


def send_notification_to_telegram(message):
    requests.get(api_url, params={'text': message, 'chat_id': my_chat_id})
