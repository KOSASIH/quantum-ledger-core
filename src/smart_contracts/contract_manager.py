import json
import os
from web3 import Web3
from solcx import compile_source, install_solc

# Install the specific version of Solidity compiler
install_solc('0.8.0')

class ContractManager:
    def __init__(self, provider_url, contract_source):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_source = contract_source
        self.contract = None
        self.contract_address = None
        self.account = None

    def set_account(self, private_key):
        """Set the account for transactions."""
        self.account = self.w3.eth.account.from_key(private_key)

    def compile_contract(self):
        """Compile the smart contract."""
        compiled_sol = compile_source(self.contract_source)
        contract_interface = compiled_sol['<stdin>:ContractTemplate']
        return contract_interface

    def deploy_contract(self):
        """Deploy the smart contract."""
        contract_interface = self.compile_contract()
        contract = self.w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']
        )

        # Build transaction
        tx = contract.constructor().buildTransaction({
            'chainId': 1,  # Mainnet
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
        })

        # Sign and send transaction
        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.privateKey)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)

        self.contract_address = tx_receipt.contractAddress
        self.contract = self.w3.eth.contract(address=self.contract_address, abi=contract_interface['abi'])
        print(f"Contract deployed at address: {self.contract_address}")

    def store_data(self, content):
        """Store data in the smart contract."""
        tx = self.contract.functions.storeData(content).buildTransaction({
            'chainId': 1,
            'gas': 200000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
            'nonce': self.w3.eth.getTransactionCount(self.account.address),
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, self.account.privateKey)
 tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        print(f"Data stored: {content}")

    def get_data(self, id):
        """Get data from the smart contract."""
        data = self.contract.functions.getData(id).call()
        return data

if __name__ == "__main__":
    provider_url = 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID'
    contract_source = open('contract_template.sol', 'r').read()
    manager = ContractManager(provider_url, contract_source)
    manager.set_account('YOUR_PRIVATE_KEY')
    manager.deploy_contract()
    manager.store_data('Hello, World!')
    data = manager.get_data(1)
    print(f"Data retrieved: {data}")
