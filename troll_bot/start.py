import logging
import os

import telegram

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from troll_bot import bot, WEBHOOK_URI
from troll_bot.handler import app


log = logging.getLogger(__name__)


def start_bot_service():
    set_webhook(bot)
    start_tornado(app)


def set_webhook(bot):
    base_url = os.environ['BOT_URL']
    webhook_url = base_url + WEBHOOK_URI
    log.info('Setting URL: %s', webhook_url)

    certificate_path = os.environ['CERTIFICATE_PATH']
    
    with open(certificate_path, 'rb') as certificate:
        bot.setWebhook(webhook_url, certificate)


def start_tornado(app):
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()