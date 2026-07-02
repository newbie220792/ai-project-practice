 
from app.config import BOT_TOKEN, CHAT_ID
import requests

def sendTelegramMessage(message):
    # url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=html&text={message}"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "html"
    }

    response = requests.post(url, json=payload)
    return response.json()