import os
import logging

from flask import request, g
import telegram

from troll_bot import WEBHOOK_URI, bot
from troll_bot.database import app

@app.route(WEBHOOK_URI, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True))
        message_json = update.message.to_dict()

        db = g.db_client['troll-bot']
        logging.info('Insert message:%s', message_json)
        db.messages.insert_one(message_json)

        chat_id = update.message.chat.id
        message_id = update.message.message_id

        text = update.message.text

        bot.forwardMessage(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)

    return 'ok'
