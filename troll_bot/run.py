import logging
import os
import time

from telegram import Updater

from troll_bot import CERTIFICATE_PATH, BOT_URL
from troll_bot.handler import update_handler
from troll_bot.utils import generate_random_string


log = logging.getLogger(__name__)


def run_bot_service():
    token = os.environ['BOT_TOKEN']
    updater = Updater(token, workers=10)

    updater.dispatcher.addTelegramMessageHandler(update_handler)

    if CERTIFICATE_PATH:
        webhook_path = generate_random_string(length=20)
        webhook_uri = '/' + webhook_path
        set_webhook(updater, webhook_uri)
        update_queue = updater.start_webhook('0.0.0.0', 5000, webhook_path)
    else:
        update_queue = updater.start_polling(poll_interval=0.1, timeout=10)

    running = True
    while running:
        try:
            time.sleep(20000)
        except KeyboardInterrupt:
            running = False
    updater.stop()

def set_webhook(updater, webhook_uri):
    base_url = BOT_URL
    webhook_url = base_url + webhook_uri
    log.info('Setting URL: %s', webhook_url)

    certificate_path = CERTIFICATE_PATH
    
    updater.bot.setWebhook(webhook_url, open(certificate_path, 'rb'))
