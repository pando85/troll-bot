import os
import logging

from pymongo import MongoClient


HOST = os.environ['DB_HOST']
PORT = int(os.environ['DB_PORT'])

client = MongoClient(HOST, PORT)
db = client['troll-bot']


def save_message(message):
    message_json = message.to_dict()
    logging.info('Save message: %s', message_json)
    db.messages.insert_one(message_json)

def search_messages(words, chat_id=None):
    if type(words) is not list:
        logging.debug('words is not list, transforming to list')
        words = [words]

    logging.debug('words: %s', words)
    contain_words = get_contain_words_regex(words)

    search_dict = {}
    search_dict['text'] = contain_words

    if chat_id:
        logging.debug("chat_id: %s", chat_id)
        search_dict['chat.id'] = chat_id

    logging.debug('Search dict: %s', search_dict)
    message_list = list(db.messages.find( search_dict ))
    logging.debug("Message list: %s", message_list)

    return message_list

def get_contain_words_regex(words):
    regex = r'^' + ''.join([ r'(?=.*\b' + word + r'\b)' for word in words]) + r'.*$'

    logging.debug('Regex : %s', regex)

    contain_words = {'$regex': regex, '$options' : 'i'}
    logging.debug("Regex: %s", contain_words)

    return contain_words
