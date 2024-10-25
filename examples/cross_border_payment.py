import os
import logging
import requests
from web3 import Web3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CrossBorderPayment:
    def __init__(self, provider_url, exchange_rate_api):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.exchange_rate_api = exchange_rate_api

    def get_exchange_rate(self, from_currency, to_currency):
        """Get the exchange rate between two currencies."""
        response = requests.get(f"{self .exchange_rate_api}/{from_currency}/{to_currency}")
        response.raise_for_status()
        return response.json()["rate"]

    def process_transaction(self, from_address, to_address, amount, from_currency, to_currency):
        """Process a cross-border payment transaction."""
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)
        converted_amount = amount * exchange_rate

        # Convert the amount to the target currency
        logger.info(f"Converting {amount} {from_currency} to {converted_amount} {to_currency}")

        # Send the transaction
        tx = {
            'to': to_address,
            'value': self.w3.toWei(converted_amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(from_address),
        }
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.w3.eth.accounts[0].privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        logger.info(f"Transaction sent with hash: {tx_hash.hex()}")

if __name__ == "__main__":
    PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
    EXCHANGE_RATE_API = os.getenv("EXCHANGE_RATE_API", "https://api.exchangerate-api.com/v4/latest")

    payment_system = CrossBorderPayment(PROVIDER_URL, EXCHANGE_RATE_API)

    # Process a cross-border payment transaction
    payment_system.process_transaction(
        "0xSenderAddressHere",
        "0xRecipientAddressHere",
        100,  # Amount in USD
        "USD",
        "EUR"
    )
