import hashlib
import json
import random

class Consensus:
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def proof_of_work(self, last_proof):
        proof = 0
        while not self.valid_proof(last_proof, proof):
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"  # Difficulty level can be adjusted

    def consensus_algorithm(self):
        # Example of a simple voting-based consensus algorithm
        votes = {}
        for node in self.blockchain.nodes:
            # Simulate voting process
            vote = self.get_vote_from_node(node)
            votes[vote] = votes.get(vote, 0) + 1

        # Determine the most voted chain
        most_voted_chain = max(votes, key=votes.get)
        return most_voted_chain

    def get_vote_from_node(self, node):
        # Simulate a node's vote (in a real scenario, this would involve network communication)
        return random.choice(self.blockchain.chain)  # Randomly voting for a block in the chain

    def validate_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.blockchain.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            last_block = block
            current_index += 1
        return True
