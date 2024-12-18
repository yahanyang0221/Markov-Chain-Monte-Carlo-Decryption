import unittest
from cipher_utils import (
    generate_random_cipher,
    create_mapping_from_cipher,
    encrypt,
    decrypt
)
import string


class TestCipherUtils(unittest.TestCase):

    def setUp(self):
        """
        Set up common variables for testing.
        """
        self.text = "hello world"
        self.cipher = generate_random_cipher()  # Random cipher
        self.mapping = create_mapping_from_cipher(self.cipher)

    def test_generate_random_cipher(self):
        """
        Test that the generated cipher is valid and random.
        """
        cipher1 = generate_random_cipher()
        cipher2 = generate_random_cipher()

        # Should have 26 unique characters
        self.assertEqual(len(cipher1), 26)
        # All characters must be unique
        self.assertEqual(len(set(cipher1)), 26)
        # Successive ciphers should differ
        self.assertNotEqual(cipher1, cipher2)

    def test_create_mapping_from_cipher(self):
        """
        Test that the mapping correctly matches the cipher.
        """
        alphabet = string.ascii_lowercase
        mapping = create_mapping_from_cipher(self.cipher)

        # Check all keys and values
        for char, mapped_char in zip(alphabet, self.cipher):
            self.assertEqual(mapping[char], mapped_char)

    def test_encrypt(self):
        """
        Test that text is encrypted correctly.
        """
        encrypted_text = encrypt(self.text, self.mapping)

        # Ensure the length of encrypted text matches the original
        self.assertEqual(len(encrypted_text), len(self.text))

        # Ensure the encrypted text differs from the original text
        self.assertNotEqual(self.text, encrypted_text)

        # Ensure encryption is reversible
        decrypted_text = decrypt(encrypted_text, self.mapping)
        self.assertEqual(self.text, decrypted_text)

    def test_decrypt(self):
        """
        Test that text is decrypted correctly.
        """
        encrypted_text = encrypt(self.text, self.mapping)
        decrypted_text = decrypt(encrypted_text, self.mapping)

        # Ensure the decrypted text matches the original
        self.assertEqual(self.text, decrypted_text)

    def test_encrypt_decrypt_with_non_alphabet_characters(self):
        """
        Test non-alphabet characters are preserved
        during encryption and decryption.
        """
        text_with_specials = "hello world! 123."
        encrypted_text = encrypt(text_with_specials, self.mapping)
        decrypted_text = decrypt(encrypted_text, self.mapping)

        # Ensure the decrypted text matches the original
        self.assertEqual(text_with_specials, decrypted_text)

        # Ensure non-alphabet characters are not encrypted
        for char in "! 123.":
            self.assertIn(char, encrypted_text)


if __name__ == "__main__":
    unittest.main()
