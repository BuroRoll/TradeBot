import requests

from settings import settings

telegram_api_token = settings.TELEGRAM_API_TOKEN
my_chat_id = settings.TELEGRAM_CHAT_ID

api_url = f'https://api.telegram.org/bot{telegram_api_token}/sendMessage'


def send_notification_to_telegram(message) -> None:
    requests.get(api_url, params={'text': message, 'chat_id': my_chat_id})
