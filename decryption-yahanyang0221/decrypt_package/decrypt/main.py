import sys
from preprocessing import preprocess_text, compute_bigram_frequencies
from mcmc import run_mcmc
from cipher_utils import decrypt, create_mapping_from_cipher
from line_profiler import profile


@profile
def main():
    if len(sys.argv) != 4:
        print("Usage: python main.py <path to file to decode> \
              <number of iterations> <path to reference document>")
        sys.exit(1)

    file_to_decode_path = sys.argv[1]
    iterations = int(sys.argv[2])
    reference_file_path = sys.argv[3]

    with open(file_to_decode_path, "r") as f:
        encrypted_text = preprocess_text(f.read())

    with open(reference_file_path, "r") as f:
        reference_text = preprocess_text(f.read())

    # step 1: Compute bigram frequencies of reference text
    bigram_freq = compute_bigram_frequencies(reference_text)

    # step 2: use mcmc algo to find best key and score
    best_key, best_score = run_mcmc(encrypted_text, bigram_freq, iterations)

    # step 3: use the best key to create mapping
    best_mapping = create_mapping_from_cipher(best_key)

    # step 4: decrypt encrypted text
    decrypted_text = decrypt(encrypted_text, best_mapping)

    print("Decrypted Text:")
    print(decrypted_text)
    print("Best Key:", best_key)
    print("Best Score:", best_score)

    with open("some_text_decrypted.txt", "w") as f:
        f.write(decrypted_text)


if __name__ == "__main__":
    main()
