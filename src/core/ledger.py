import json
import os

class Ledger:
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.ledger_file = 'ledger.json'
        self.load_ledger()

    def load_ledger(self):
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, 'r') as file:
                self.blockchain.chain = json.load(file)

    def save_ledger(self):
        with open(self.ledger_file, 'w') as file:
            json.dump(self.blockchain.chain, file)

    def add_block(self, block):
        self.blockchain.chain.append(block)
        self.save_ledger()

    def get_balance(self, address):
        balance = 0
        for block in self.blockchain.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address:
                    balance -= transaction['amount']
                if transaction['recipient'] == address:
                    balance += transaction['amount']
        return balance

    def get_transaction_history(self, address):
        history = []
        for block in self.blockchain.chain:
            for transaction in block['transactions']:
                if transaction['sender'] == address or transaction['recipient'] == address:
                    history.append(transaction)
        return history
