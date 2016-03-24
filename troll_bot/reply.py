import logging
import os
import random


from troll_bot.audio import send_audio
from troll_bot.gif import send_gif
from troll_bot.database import search_messages_by_word
from troll_bot.utils import return_true_by_percentaje, random_item


log = logging.getLogger(__name__)


def should_reply():
    return return_true_by_percentaje(5)

def get_random_word(message_received):
    message_words = message_received.text.split()
    log.debug('Message words: %s', message_words)

    random_word = random_item(message_words)

    return random_word


def get_reply_message(random_word):

    possible_messages = search_messages_by_word(random_word)[:-1]

    if len(possible_messages) == 0:
        log.debug('No possible messages to reply.')
        return

    reply_message = random_item(possible_messages)
    log.debug('Reply message: %s', reply_message)

    return reply_message

def get_reply_type():
    case = random.randint(1, 100)

    if case <= 80:
        return 'text'
    if case <= 90:
        return 'gif'
    if case > 90:
        return 'audio'

def reply_text_message(bot, reply_message, chat_id):
    bot.forwardMessage(chat_id=chat_id,
        from_chat_id=reply_message['chat']['id'], message_id=reply_message['message_id'])

def reply_audio_message(bot, chat_id, reply_message):
    send_audio(bot, chat_id, reply_message)

def reply_gif_message(bot, chat_id, reply_word):
    send_gif(bot, chat_id, reply_word)