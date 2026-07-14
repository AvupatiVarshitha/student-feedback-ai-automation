import requests

from backend.config import TELEGRAM_BOT_TOKEN


def send_message(chat_id, message):
    """
    Send a Telegram message to any batch group.
    """

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {

        "chat_id": chat_id,

        "text": message,

        "parse_mode": "HTML"

    }

    response = requests.post(
        url,
        json=payload
    )

    return response.json()