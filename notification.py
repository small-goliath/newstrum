import os
import requests
from logger import get_logger
from dotenv import load_dotenv

log = get_logger('notofication')
load_dotenv()

discord_webhook = os.getenv('discord_webhook')
hangout_webhook = os.getenv('hangout_webhook')

def send_to_discord(message: str):
    # message = message.replace('**', '__')
    if not discord_webhook:
        return
    
    if len(message) > 2000:
        message = message[:1994] + "...```"

    data = {
        "content": message
    }

    response = requests.post(discord_webhook, json=data)

    if response.status_code == 204:
        log.info("🔔 메시지가 Discord에 성공적으로 전송되었습니다.")
    else:
        log.error(f"❌ Discord 전송 실패: {response.status_code} - {response.text}")

import requests

def send_to_hangout(message: str):
    # message = message.replace('**', '*')
    data = {
        "text": message
    }

    response = requests.post(hangout_webhook, json=data)

    if response.status_code == 200:
        log.info("🔔 메시지가 Google Chat에 성공적으로 전송되었습니다.")
    else:
        log.error(f"❌ Google Chat 전송 실패: {response.status_code} - {response.text}")
