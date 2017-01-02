import logging

from telegram.ext.dispatcher import run_async
from telegram.ext import MessageHandler, Filters

from troll_bot.database import save_message
from troll_bot.reply import (get_random_word, get_reply_message, should_reply, get_reply_type,
                             reply_text_message, reply_audio_message, reply_gif_message)
log = logging.getLogger(__name__)


def get_update_handler():
    return MessageHandler(Filters.text, reply_text)

@run_async
def reply_text(bot, received, **kwargs):
    log.debug('Received: %s', received)

    save_message(received.message)

    if not hasattr(received.message, 'text'):
        log.info('Not text message received.')
        return

    if not should_reply():
        return

    random_word = get_random_word(received.message)
    reply_message = get_reply_message(random_word, received.message.chat.id)
    if not reply_message:
        log.info('Not reply message')
        return

    reply_type = get_reply_type()

    if reply_type == 'text':
        reply_text_message(bot, received.message.chat.id ,reply_message)

    if reply_type == 'audio':
        reply_audio_message(bot, received.message.chat.id, reply_message)

    if reply_type == 'gif':
        reply_gif_message(bot, received.message.chat.id, random_word)
