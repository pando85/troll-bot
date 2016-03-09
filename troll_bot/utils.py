import os
import binascii

def generate_random_string(length):
    random_bits = os.urandom(length)
    random_string = binascii.hexlify(random_bits)
    return random_string.decode('utf-8')