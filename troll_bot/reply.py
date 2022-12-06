import logging
import random
import datetime

from troll_bot.audio import send_audio
from troll_bot.gif import send_gif
from troll_bot.database import search_messages
from troll_bot.utils import return_true_by_percentage, random_item


log = logging.getLogger(__name__)


def should_reply():
    return return_true_by_percentage(5)


def get_random_message_word(message_received):
    message_words = message_received.text.split()
    log.debug('Message words: %s', message_words)

    random_word = random_item(message_words)

    return random_word


def get_reply_message(words_list, chat_id):
    possible_messages = search_messages(words_list, chat_id)

    possible_messages = remove_last_if_young(possible_messages)

    if not possible_messages:
        log.debug('No possible messages to reply.')
        return

    reply_message = random_item(possible_messages)
    log.debug('Reply message: %s', reply_message)

    return reply_message


def remove_last_if_young(messages):
    if not messages:
        return

    last_message_datetime = datetime.datetime.fromtimestamp(messages[-1]['date'])
    last_message_ago = datetime.datetime.now() - last_message_datetime

    logging.debug('seconds from last message: %s', last_message_ago.seconds)
    if last_message_ago.seconds < 2:
        logging.debug('Removing last message from reply, too young')
        return messages[:-1]

    return messages


def get_reply_type():
    case = random.randint(1, 100)

    if case <= 80:
        return 'text'
    if case <= 90:
        return 'gif'
    if case > 90:
        return 'audio'


def reply_text_message(bot, chat_id, reply_message):
    log.debug('Reply message: %s', reply_message)
    log.debug('Chat_id: %s', chat_id)
    bot.forwardMessage(
        chat_id=chat_id,
        from_chat_id=reply_message['chat']['id'],
        message_id=reply_message['message_id'])


def reply_audio_message(bot, chat_id, reply_message):
    send_audio(bot, chat_id, reply_message['text'])


def reply_gif_message(bot, chat_id, reply_word):
    send_gif(bot, chat_id, reply_word)
