import unittest
import time
from blockchain import Blockchain
from transaction import Transaction

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.blockchain = Blockchain()
        self.num_transactions = 1000  # Number of transactions to test

    def test_block_creation_performance(self):
        """Test the performance of block creation."""
        start_time = time.time()
        
        for _ in range(self.num_transactions):
            previous_hash = self.blockchain.get_last_block().hash
            self.blockchain.create_block(previous_hash)
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken to create {self.num_transactions} blocks: {duration:.4f} seconds")
        self.assertLess(duration, 5, "Block creation took too long!")  # Example threshold

    def test_transaction_processing_performance(self):
        """Test the performance of processing transactions."""
        start_time = time.time()
        
        for _ in range(self.num_transactions):
            transaction = Transaction(sender="Alice", recipient="Bob", amount=50)
            self.blockchain.add_transaction(transaction)
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"Time taken to process {self.num_transactions} transactions: {duration:.4f} seconds")
        self.assertLess(duration, 5, "Transaction processing took too long!")  # Example threshold

if __name__ == '__main__':
    unittest.main()
