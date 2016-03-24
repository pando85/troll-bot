import logging
import os

from telegram.dispatcher import run_async

from troll_bot.database import save_message
from troll_bot.reply import reply_message, reply_text_to_speech, reply_audio_file
from troll_bot.utils import return_true_by_percentage


log = logging.getLogger(__name__)


@run_async
def update_handler(bot, received, **kwargs):
    log.debug('Received: %s', received)

    save_message(received.message)

    if not should_reply():
        return

    if should_reply_text():
        reply_message(bot, received.message)

    if should_reply_text_to_speech():
        reply_text_to_speech(bot, received.message)

    if should_reply_audio():
        reply_audio_file(bot, received.message)


def should_reply():
    return True
    return return_true_by_percentage(5)


def should_reply_text():
    return return_true_by_percentage(90)


def should_reply_text_to_speech():
    return os.name != "nt" and return_true_by_percentage(10)


def should_reply_audio():
    return return_true_by_percentage(10)
