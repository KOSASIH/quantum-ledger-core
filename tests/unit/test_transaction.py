import unittest
from transaction import Transaction

class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.transaction = Transaction(sender="Alice", recipient="Bob", amount=50)

    def test_transaction_creation(self):
        self.assertEqual(self.transaction.sender, "Alice")
        self.assertEqual(self.transaction.recipient, "Bob")
        self.assertEqual(self.transaction.amount, 50)

    def test_transaction_validation(self):
        self.assertTrue(self.transaction.is_valid())

        # Modify the transaction to make it invalid
        self.transaction.amount = -10
        self.assertFalse(self.transaction.is_valid())

if __name__ == '__main__':
    unittest.main()
