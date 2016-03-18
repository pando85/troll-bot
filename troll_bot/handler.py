import logging
import random
import re

from flask import request, g
import telegram

from troll_bot import WEBHOOK_URI, bot
from troll_bot.database import app, save_message

log = logging.getLogger(__name__)

@app.route(WEBHOOK_URI, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        db = g.db_client['troll-bot']
        
        received = telegram.Update.de_json(request.get_json(force=True))
        save_message(received.message, db)

        if should_reply():
            reply_message = get_reply_message(received.message, db.messages)
            bot.forwardMessage(chat_id=received.message.chat.id, 
                from_chat_id=reply_message['chat']['id'], message_id=reply_message['message_id'])

    return 'ok'


def should_reply():
    percentage = 5
    case = random.randint(1, 100)
    
    if case <= percentage:
        log.info('Replying message')
        return True

    return False


def get_reply_message(message_received, db_messages):
    if not message_received.text:
        log.info('No text in message received.')
        return

    message_words = message_received.text.split()
    log.debug('Message words: %s', message_words)

    random_word = random_item(message_words)

    contain_word = re.compile(r'\b{word}\b'.format(word=random_word))
    possible_messages = list(db_messages.find({'text': contain_word}))[:-1]

    if len(possible_messages) == 0:
        log.info('No possible messages to reply.')
        return

    reply_message = random_item(possible_messages)

    return reply_message


def random_item(list_):
    items = len(list_)
    id_ = random.randint(0, items - 1)
    logging.debug('Item chosen: %s', list_[id_])

    return list_[id_]
