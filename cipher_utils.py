'''
This module handles the encryption and decryption of text using cipher.
'''

import random
import string


# generate a random cipher to encrypt
def generate_random_cipher():
    """
    Generates a random cipher string.
    """
    charset = list(string.ascii_lowercase)
    random.shuffle(charset)
    return ''.join(charset)


def create_mapping_from_cipher(cipher):
    """
    Creates the mapping between the alphabet and the cipher string using key.
    """
    charset = list(string.ascii_lowercase)
    return {original: substituted for original,
            substituted in zip(charset, cipher)}


def encrypt(text, key):
    """
    Encrypts a given text using a substitution key.
    """
    return ''.join(key.get(char, char) for char in text)


def decrypt(text, key):
    """
    Decrypts a given text using the inverse of a substitution key.
    """
    reverse_key = {v: k for k, v in key.items()}  # invert the key
    return ''.join(reverse_key.get(char, char) for char in text)
