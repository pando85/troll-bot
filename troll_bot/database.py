import os
import logging
import re

from pymongo import MongoClient


HOST = os.environ.get('DB_HOST', "127.0.0.1")
PORT = int(os.environ.get('DB_PORT', "27017"))

STORE_AUDIO_DIR = os.environ.get("STORE_AUDIO_DIR")

client = MongoClient(HOST, PORT)
db = client['troll-bot']


def save_message(message):
    message_json = message.to_dict()
    logging.info('Save message: %s', message_json)
    db.messages.insert_one(message_json)


def save_audio_message(bot, message):
    if message.voice is None or STORE_AUDIO_DIR is None:
        return

    file_id = message.voice.file_id
    target_audio_file = bot.getFile(file_id)
    target_audio_file.download(get_voice_file_name(message))


def get_voice_file_name(message):
    date = message.forward_date if message.forward_date is not None else message.date
    file_name = date.strftime("audio_%Y%m%d_%H%M%S") + ".ogg"
    return os.path.join(STORE_AUDIO_DIR, file_name)


def search_messages_by_word(query):
    contain_word = re.compile(r'\b{word}\b'.format(word=query), re.IGNORECASE)
    message_list = list(db.messages.find({'text': contain_word}))

    return message_list
