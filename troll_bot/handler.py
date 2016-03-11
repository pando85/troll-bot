import logging
import random
import re

from flask import request, g
import telegram

from troll_bot import WEBHOOK_URI, bot
from troll_bot.database import app, save_message


@app.route(WEBHOOK_URI, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True))
        
        db = g.db_client['troll-bot']
        save_message(update.message, db)

        if should_reply():
            forward_random_message(db.messages, update.message)

    return 'ok'


def should_reply():
    percentage = 5
    case = random.randint(1, 100)
    
    if case <= percentage:
        return True

    return False


def forward_random_message(db_messages, message_received):
    chat_id = message_received.chat.id
    text = message_received.text

    if not text:
        return

    words = text.split()

    random_word = random_item(words)

    contain_word = re.compile(r'\b{word}\b'.format(word=random_word))
    posible_messages = list(db_messages.find({'text': contain_word}))
    forward_message = random_item(posible_messages)

    bot.forwardMessage(chat_id=chat_id, from_chat_id=forward_message['chat']['id'],
        message_id=forward_message['message_id'])


def random_item(list_):
    items = len(list_)
    id_ = random.randint(0, items - 1)
    logging.debug('Item chosen: %s', list_[id_])

    return list_[id_]
