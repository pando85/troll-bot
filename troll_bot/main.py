import logging
import sys

from docopt import docopt


log = logging.getLogger(__name__)
console_handler = logging.StreamHandler(sys.stderr)


def main():
    """Troll Bot - Annoy your friends with this Telegram Bot.
    Usage:
      troll-bot [options]
      troll-bot (-h | --help)

    Options:
      --verbose     Show more output
    """
    setup_logging()
    arguments = docopt(main.__doc__)
    setup_console_handler(console_handler, arguments.get('--verbose'))


def setup_logging():
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)


def setup_console_handler(handler, verbose):
    if verbose:
        handler.setLevel(logging.DEBUG)
    else:
        handler.setLevel(logging.INFO)        
