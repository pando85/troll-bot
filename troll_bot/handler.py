import os
import logging

from flask import Flask, request
import telegram

from troll_bot import (WEBHOOK_URI, bot)


app = Flask(__name__)


@app.route(WEBHOOK_URI, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = telegram.Update.de_json(request.get_json(force=True))

        chat_id = update.message.chat.id
        message_id = update.message.message_id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text

        if text:
            # repeat the same message back (echo)
            bot.forwardMessage(chat_id=chat_id, from_chat_id=chat_id, message_id=message_id)

    return 'ok'
