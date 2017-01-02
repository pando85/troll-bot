import os
import logging
import re

from pymongo import MongoClient


HOST = os.environ['DB_HOST']
PORT = int(os.environ['DB_PORT'])

client = MongoClient(HOST, PORT)
db = client['troll-bot']


def save_message(message):
    message_json = message.to_dict()
    logging.info('Save message: %s', message_json)
    db.messages.insert_one(message_json)

def search_messages_by_word_in_chat_id(query, chat_id):
    contain_word = get_contain_word_regex(query)
    logging.debug("chat_id: %s", chat_id)
    message_list = list(db.messages.find({'text': contain_word, 'chat.id': chat_id} ))
    logging.debug("Message list: %s", message_list)

    return message_list

def search_messages_by_word(query):
    contain_word = get_contain_word_regex(query)
    message_list = list(db.messages.find({'text': contain_word}))

    return message_list

def get_contain_word_regex(word):
    contain_word = re.compile(r'\b{word}\b'.format(word=word), re.IGNORECASE)
    logging.debug("Regex: %s", contain_word)

    return contain_word
