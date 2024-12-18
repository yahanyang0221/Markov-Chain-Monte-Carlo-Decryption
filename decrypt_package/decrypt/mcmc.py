'''
This module handles the MCMC decryption algorithm and related computations.
'''

import math
import random
from cipher_utils import generate_random_cipher, decrypt
from cipher_utils import create_mapping_from_cipher
from line_profiler import profile


@profile
def compute_log_likelihood(document, bigram_freq, default_prob=1e-6):
    """
    Computes the log-likelihood of reference text using bigram frequencies.
    """
    log_likelihood = 0
    for i in range(1, len(document)):
        c1, c2 = document[i - 1], document[i]
        prob = bigram_freq.get((c1, c2), default_prob)
        log_likelihood += math.log(prob)
    return log_likelihood


@profile
def compute_score(key, encrypted_text, bigram_freq):
    """
    Computes the score for a given decryption key.
    """
    # Convert the string cipher into a dictionary mapping
    decryption_key = create_mapping_from_cipher(key)

    # Decrypt the text and compute the log-likelihood
    decrypted_text = decrypt(encrypted_text, decryption_key)
    return compute_log_likelihood(decrypted_text, bigram_freq)


@profile
def propose_cipher(current_cipher):
    """
    Proposes a new cipher by swapping two characters.
    """
    first_letter = random.choice(current_cipher)
    second_letter = random.choice(current_cipher)

    while first_letter == second_letter:
        second_letter = random.choice(current_cipher)

    new_cipher = ""
    for c in current_cipher:
        if c == first_letter:
            new_cipher += second_letter
        elif c == second_letter:
            new_cipher += first_letter
        else:
            new_cipher += c

    return new_cipher


@profile
def metropolis_step(current_key, current_score,
                    encrypted_text, bigram_freq, p=1.0):
    """
    Performs one step of the Metropolis-Hastings algorithm.
    """
    candidate_key = propose_cipher(current_key)
    candidate_score = compute_score(candidate_key, encrypted_text, bigram_freq)

    acceptance_probability = min(1, (math.exp(candidate_score -
                                              current_score))**p)

    if random.random() < acceptance_probability:
        return candidate_key, candidate_score
    else:
        return current_key, current_score


@profile
def run_mcmc(encrypted_text, bigram_freq, iterations, p=1.0):
    """
    Runs the MCMC decryption algorithm for a specified number of iterations.
    """
    current_cipher = generate_random_cipher()
    current_score = compute_score(current_cipher, encrypted_text, bigram_freq)

    best_cipher = current_cipher
    best_score = current_score

    for _ in range(iterations):
        current_cipher, current_score = metropolis_step(
            current_cipher, current_score, encrypted_text, bigram_freq, p
        )
        if current_score > best_score:
            best_cipher, best_score = current_cipher, current_score

    return best_cipher, best_score
