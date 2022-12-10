import logging
import os
import time

from telegram.ext import Updater

from troll_bot import CERTIFICATE_PATH, BOT_URL
from troll_bot.handler import get_update_handler, get_forward_handler, get_help_handler
from troll_bot.utils import generate_random_string


log = logging.getLogger(__name__)


def run_bot_service():
    token = os.environ['BOT_TOKEN']
    updater = Updater(token, workers=10)

    updater.dispatcher.add_handler(get_update_handler())
    updater.dispatcher.add_handler(get_forward_handler())
    updater.dispatcher.add_handler(get_help_handler())

    if BOT_URL:
        webhook_path = generate_random_string(length=20)
        webhook_uri = '/' + webhook_path
        set_webhook(updater, webhook_uri)
        updater.start_webhook('0.0.0.0', 5000, webhook_path)
    else:
        updater.start_polling(poll_interval=0.1, timeout=10)

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

    if CERTIFICATE_PATH:
        updater.bot.setWebhook(webhook_url, open(CERTIFICATE_PATH, 'rb'))
    else:
        updater.bot.setWebhook(webhook_url)

