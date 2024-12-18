'''
This module handles the preprocessing of reference text.
'''
import string
from collections import Counter


def preprocess_text(text):
    """
    Preprocesses the input text by converting to lowercase,
    removing special characters, and normalizing spaces.
    """
    text = text.lower()
    allowed_chars = set(string.ascii_lowercase + " ")
    text = ''.join(char if char in allowed_chars else ' ' for char in text)
    text = ' '.join(text.split())
    return text


def compute_bigram_frequencies(text):
    """
    Computes the frequencies of bigrams
    (pairs of consecutive characters) in the given reference text.
    """
    text = preprocess_text(text)

    # Count bigrams
    bigrams = zip(text, text[1:])
    bigram_counts = Counter(bigrams)

    # Normalize counts
    total_bigrams = sum(bigram_counts.values())
    bigram_freq = {bigram: count / total_bigrams for bigram,
                   count in bigram_counts.items()}

    return bigram_freq
