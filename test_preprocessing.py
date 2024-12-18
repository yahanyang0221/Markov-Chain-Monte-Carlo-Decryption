import unittest
from preprocessing import preprocess_text, compute_bigram_frequencies


class TestPreprocessing(unittest.TestCase):

    def test_preprocess_text_lowercase(self):
        """
        Test that the text is correctly converted to lowercase.
        """
        text = "HELLO WORLD"
        processed_text = preprocess_text(text)
        self.assertEqual(processed_text, "hello world")

    def test_preprocess_text_special_characters(self):
        """
        Test that special characters are removed from the text.
        """
        text = "Hello, World! How's it going?"
        processed_text = preprocess_text(text)
        self.assertEqual(processed_text, "hello world how s it going")

    def test_preprocess_text_extra_spaces(self):
        """
        Test that extra spaces are normalized to a single space.
        """
        text = "Hello    World   "
        processed_text = preprocess_text(text)
        self.assertEqual(processed_text, "hello world")

    def test_compute_bigram_frequencies_complex(self):
        """
        Test the computation of bigram frequencies for a complex input.
        """
        text = "hello world"
        bigram_freq = compute_bigram_frequencies(text)
        # Check that the bigram frequencies sum to 1
        total_frequency = sum(bigram_freq.values())
        self.assertAlmostEqual(total_frequency, 1.0)

        # Check for specific bigrams
        self.assertIn(('h', 'e'), bigram_freq)
        self.assertIn(('e', 'l'), bigram_freq)

    def test_compute_bigram_frequencies_with_spaces(self):
        """
        Test the computation of bigram frequencies with spaces in the input.
        """
        text = "hi there"
        bigram_freq = compute_bigram_frequencies(text)
        self.assertIn(('h', 'i'), bigram_freq)
        self.assertIn(('i', ' '), bigram_freq)
        self.assertIn((' ', 't'), bigram_freq)


if __name__ == "__main__":
    unittest.main()
