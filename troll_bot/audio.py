import os
import subprocess

from troll_bot.espeak import ESpeak
from troll_bot.utils import generate_random_string


def get_text_to_speech_file(text):
    tmp_file_path = '/tmp/{path}.wav'.format( path = generate_random_string(20))
    espeak = ESpeak(voice='es+m2')

    espeak.save(text, tmp_file_path)
    ogg_tmp_file_path = transcode_to_ogg(tmp_file_path)
    return ogg_tmp_file_path


def transcode_to_ogg(file_path):
    output_file_path = '{path}.ogg'.format( path = remove_extension(file_path))
    oggenc_cmd = ['oggenc', '-q3', '-o', output_file_path, file_path]
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.check_call(oggenc_cmd, stdout=FNULL, stderr=subprocess.STDOUT)
    except:
        raise
    finally:
        os.remove(file_path)

    return output_file_path


def remove_extension(file_path):
    file_path_without_extension, extension = os.path.splitext(file_path)
    return file_path_without_extension
