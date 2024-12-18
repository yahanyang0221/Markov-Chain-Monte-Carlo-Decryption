import unittest
from mcmc import (
    compute_log_likelihood,
    compute_score,
    propose_cipher,
    metropolis_step,
    run_mcmc
)
from cipher_utils import generate_random_cipher, create_mapping_from_cipher
from preprocessing import preprocess_text, compute_bigram_frequencies


class TestMCMC(unittest.TestCase):

    def setUp(self):
        """
        Set up test data and dependencies.
        """
        # Example reference text
        self.reference_text = "this is a sample reference text"
        self.bigram_freq = compute_bigram_frequencies(self.reference_text)

        # Example encrypted text
        self.encrypted_text = "xmqfx ym x tzqqfz mqixfykz xzxq"

        # Example cipher
        self.cipher = generate_random_cipher()
        self.mapping = create_mapping_from_cipher(self.cipher)

    def test_compute_log_likelihood(self):
        """
        Test that log-likelihood computation is correct.
        """
        preprocessed_text = preprocess_text(self.reference_text)
        likelihood = compute_log_likelihood(
            preprocessed_text, self.bigram_freq)
        self.assertIsInstance(likelihood, float)
        self.assertLessEqual(likelihood, 0)  # Log-likelihood is non-positive

    def test_compute_score(self):
        """
        Test the score computation for a given key.
        """
        score = compute_score(
            self.cipher, self.encrypted_text, self.bigram_freq)
        self.assertIsInstance(score, float)

    def test_propose_cipher(self):
        """
        Test that propose_cipher generates a valid cipher.
        """
        new_cipher = propose_cipher(self.cipher)
        # Cipher should change
        self.assertNotEqual(new_cipher, self.cipher)
        # Length should match
        self.assertEqual(len(new_cipher), len(self.cipher))
        # Should still use same characters
        self.assertCountEqual(new_cipher, self.cipher)

    def test_metropolis_step(self):
        """
        Test that Metropolis step returns a valid cipher and score.
        """
        current_score = compute_score(
            self.cipher, self.encrypted_text, self.bigram_freq)
        new_cipher, new_score = metropolis_step(
            self.cipher, current_score, self.encrypted_text, self.bigram_freq
        )
        self.assertNotEqual(new_cipher, None)
        self.assertIsInstance(new_score, float)

    def test_run_mcmc(self):
        """
        Test the full MCMC algorithm.
        """
        best_cipher, best_score = run_mcmc(
            self.encrypted_text, self.bigram_freq, iterations=100)
        self.assertIsInstance(best_cipher, str)
        # Cipher length should match alphabet
        self.assertEqual(len(best_cipher), 26)
        self.assertIsInstance(best_score, float)


if __name__ == "__main__":
    unittest.main()
