import logging
import os
from os.path import isfile, join

from troll_bot.audio import get_text_to_speech_file
from troll_bot.database import search_messages_by_word
from troll_bot.utils import return_true_by_percentaje, random_item


log = logging.getLogger(__name__)
audio_dir = os.environ["AUDIO_DIR"]

def send_recorded_audio(bot, message):
    if audio_dir == "" or audio_dir is None or not is_text_message(message):
        return

    random_word = get_random_message_word(message)
    audiofiles = [file for file in os.listdir(audio_dir) if is_audio_file(file)]

    if len(audiofiles) == 0:
        return

    send_audio_file(bot, message.chat, random_item(audiofiles))


def send_audio_file(bot, chat, audio_filename):
    audio_filepath = join(audio_dir, audio_filename)
    log.debug("Must send: " + audio_filepath)

    bot.sendVoice(chat_id=chat.id, voice=open(audio_filepath, 'rb'))


def is_audio_file(filename):
    return isfile(join(audio_dir, filename)) and filename.endswith((".mp3", ".ogg"))

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
    if not is_text_message(message_received):
        log.info('No text in message received.')
        return

    random_word = get_random_message_word(message_received)
    possible_messages = search_messages_by_word(random_word)[:-1]

    if len(possible_messages) == 0:
        log.info('No possible messages to reply.')
        return

    reply_message = random_item(possible_messages)
    log.debug('Reply message: %s', reply_message)

    return reply_message

def is_text_message(message):
    return message.text is not None


def get_random_message_word(message):
    message_words = message.text.split()
    log.debug('Message words: %s', message_words)

    return random_item(message_words)


def should_audio_reply():
    return return_true_by_percentaje(5)

