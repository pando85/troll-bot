import urllib
import os

import giphypop

from troll_bot.utils import generate_random_string


def send_gif(bot, chat_id, text):
    gif_path = get_gif_file_path(text)

    try:
        bot.sendDocument(chat_id, open(gif_path, 'br'))
    except:
        raise
    finally:
        os.remove(gif_path)

def get_gif_file_path(text):
    giphy = giphypop.Giphy()
    tmp_file_path = '/tmp/{random}.gif'.format(random=generate_random_string(20))
    gif_url = giphy.translate(text).media_url
    try:
        urllib.request.urlretrieve(gif_url, tmp_file_path)
    except:
        os.remove(tmp_file_path)
        raise

    return tmp_file_path