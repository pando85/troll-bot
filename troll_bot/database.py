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


def search_messages_by_word(query):
    contain_word = re.compile(r'\b{word}\b'.format(word=query), re.IGNORECASE)
    message_list = list(db.messages.find({'text': contain_word}))

    return message_list
