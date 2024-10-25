import hashlib
import json
from time import time

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = time()
        self.transaction_id = self.create_transaction_id()

    def create_transaction_id(self):
        transaction_string = f"{self.sender}{self.recipient}{self.amount}{self.timestamp}".encode()
        return hashlib.sha256(transaction_string).hexdigest()

    def to_dict(self):
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'recipient': self.recipient,
            'amount': self.amount,
            'timestamp': self.timestamp,
        }

class TransactionPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        if self.validate_transaction(transaction):
            self.transactions.append(transaction)
            return True
        return False

    def validate_transaction(self, transaction):
        # Basic validation rules
        if transaction.amount <= 0:
            return False
        if not transaction.sender or not transaction.recipient:
            return False
        return True

    def get_transactions(self):
        return [tx.to_dict() for tx in self.transactions]

    def clear_transactions(self):
        self.transactions = []
