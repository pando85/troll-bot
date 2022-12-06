import os
import binascii
import random
import logging


def generate_random_string(length):
    random_bits = os.urandom(length)
    random_string = binascii.hexlify(random_bits)
    return random_string.decode('utf-8')


def return_true_by_percentage(percentage):
    case = random.randint(1, 100)

    if case <= percentage:
        return True
    return False


def random_item(list_):
    items = len(list_)
    id_ = random.randint(0, items - 1)
    logging.debug('Item chosen: %s', list_[id_])

    return list_[id_]


def remove_word(words):
    removed_word = get_shortest_word(words)
    logging.debug('Removing: %s', removed_word)
    return [word for word in words if word is not removed_word]


def get_shortest_word(words):
    return min(words, key=len)
