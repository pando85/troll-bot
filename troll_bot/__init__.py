import os

import telegram

from flask import Flask
from troll_bot.utils import generate_random_string

TOKEN = os.environ['BOT_TOKEN']
bot = telegram.Bot(token=TOKEN)

WEBHOOK_URI = '/{random_string}'.format(random_string=generate_random_string(length=20))

app = Flask(__name__)