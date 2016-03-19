import logging

from telegram.dispatcher import run_async

from troll_bot.database import save_message
from troll_bot.reply import reply_message


log = logging.getLogger(__name__)


@run_async
def update_handler(bot, received, **kwargs):
    log.debug('Received: %s', received)

    save_message(received.message)
    reply_message(bot, received.message)
