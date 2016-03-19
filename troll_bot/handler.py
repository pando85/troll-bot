import logging
import re

from flask import request, g
import telegram

from troll_bot import WEBHOOK_URI
from troll_bot.database import app, save_message
from troll_bot.reply import reply_message


log = logging.getLogger(__name__)


@app.route(WEBHOOK_URI, methods=['POST'])
def webhook_handler():
    if request.method == "POST":
        db = g.db_client['troll-bot']
        received = telegram.Update.de_json(request.get_json(force=True))

        save_message(received.message, db)
        reply_message(received.message, db)

    return 'ok'
