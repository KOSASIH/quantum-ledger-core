import unittest
from crypto import Crypto

class TestCrypto(unittest.TestCase):
    def setUp(self):
        self.crypto = Crypto()
        self.data = "Hello, World!"
        self.private_key = "my_private_key"
        self.public_key = "my_public_key"

    def test_hashing(self):
        hash_value = self.crypto.hash(self.data)
        self.assertIsNotNone(hash_value)
        self.assertNotEqual(hash_value, self.data)

    def test_signature_verification(self):
        signature = self.crypto.sign(self.data, self.private_key)
        self.assertTrue(self.crypto.verify_signature(self.data, signature, self.public_key))

        # Tamper with the data
        tampered_data = "Hello, Tampered World!"
        self.assertFalse(self.crypto.verify_signature(tampered_data, signature, self.public_key))

if __name__ == '__main__':
    unittest.main()
