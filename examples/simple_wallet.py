import os
import json
import logging
from web3 import Web3
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleWallet:
    def __init__(self, provider_url):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = None

    def generate_keys(self):
        """Generate a new RSA key pair and save to files."""
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        public_key = private_key.public_key()

        # Save the private key
        with open("private_key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL
            ))

        # Save the public key
        with open("public_key.pem", "wb") as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        logger.info("Generated and saved RSA key pair.")

    def load_account(self, private_key_path):
        """Load an account from a private key file."""
        with open(private_key_path, "rb") as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        self.account = self.w3.eth.account.privateKeyToAccount(private_key)

    def check_balance(self):
        """Check the balance of the wallet."""
        if not self.account:
            logger.error("Account not loaded. Please load an account first.")
            return
        balance = self.w3.eth.get_balance(self.account.address)
        logger.info(f"Balance for {self.account.address}: {self.w3.fromWei(balance, 'ether')} ETH")

    def send_transaction(self, to_address, amount):
        """Send a transaction from the wallet."""
        if not self.account:
            logger.error("Account not loaded. Please load an account first.")
            return
        tx = {
            'to': to_address,
            'value': self.w3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logger.info(f"Transaction sent with hash: {tx_hash.hex()}")

if __name__ == "__main__":
    PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
    wallet = SimpleWallet(PROVIDER_URL)

    # Generate keys (uncomment to generate new keys)
    # wallet.generate_keys()

    # Load account from private key
    wallet.load_account("private_key.pem")

    # Check balance
    wallet.check_balance()

    # Send transaction (uncomment to send a transaction)
    # wallet.send_transaction("0xRecipientAddressHere", 0.01)
