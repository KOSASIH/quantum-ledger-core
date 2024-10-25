import unittest
from blockchain import Blockchain, Block

class TestBlockchain(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()

    def test_create_block(self):
        previous_hash = self.blockchain.get_last_block().hash
        new_block = self.blockchain.create_block(previous_hash)
        self.assertEqual(new_block.index, 1)
        self.assertEqual(new_block.previous_hash, previous_hash)

    def test_chain_validation(self):
        self.blockchain.create_block(self.blockchain.get_last_block().hash)
        self.assertTrue(self.blockchain.is_chain_valid())

        # Tamper with the blockchain
        self.blockchain.chain[1].data = "Tampered Data"
        self.assertFalse(self.blockchain.is_chain_valid())

if __name__ == '__main__':
    unittest.main()
