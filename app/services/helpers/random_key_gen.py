import random

from app.config import POSTFIX_LENGTH


def gen_rand_key(key_len: int = POSTFIX_LENGTH) -> str:
    """Generates a new key consisting of given length random chars."""
    char_selection = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    new_key = ''
    for digit in range(key_len):
        rand_ind = random.randint(0, len(char_selection) - 1)
        new_key += str(char_selection[rand_ind])

    return new_key
