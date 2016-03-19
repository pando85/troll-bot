import logging
import os

from troll_bot.audio import get_text_to_speech_file
from troll_bot.database import search_messages_by_word
from troll_bot.utils import return_true_by_percentaje, random_item


log = logging.getLogger(__name__)


def reply_message(bot, message):
    if should_reply():
        log.info('Replying message')
        reply_message = get_reply_message(message)
        if not reply_message:
            log.info('Not message to reply')
            return

        if should_audio_reply():
            audio_file_path = get_text_to_speech_file(reply_message['text'])
            try:
                bot.sendVoice(chat_id=message.chat.id, voice=open(audio_file_path, 'rb'))
            except:
                raise
            finally:
                os.remove(audio_file_path)
        else:
            bot.forwardMessage(chat_id=message.chat.id, 
                from_chat_id=reply_message['chat']['id'], message_id=reply_message['message_id'])


def should_reply():
    return return_true_by_percentaje(5)


def get_reply_message(message_received):
    if not message_received.text:
        log.info('No text in message received.')
        return

    message_words = message_received.text.split()
    log.debug('Message words: %s', message_words)

    random_word = random_item(message_words)
    possible_messages = search_messages_by_word(random_word)[:-1]

    if len(possible_messages) == 0:
        log.info('No possible messages to reply.')
        return

    reply_message = random_item(possible_messages)
    log.debug('Reply message: %s', reply_message)

    return reply_message


def should_audio_reply():
    return return_true_by_percentaje(5)