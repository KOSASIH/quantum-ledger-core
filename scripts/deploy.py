import os
import logging
from web3 import Web3
from solcx import compile_source

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Deployer:
    def __init__(self, provider_url, contract_source):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.contract_source = contract_source
        self.contract_interface = self.compile_contract()

    def compile_contract(self):
        """Compile the smart contract."""
        compiled_sol = compile_source(self.contract_source)
        return compiled_sol['<stdin>:TestContract']

    def deploy_contract(self):
        """Deploy the smart contract."""
        contract = self.w3.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        account = self.w3.eth.accounts[0]
        tx_hash = contract.constructor().transact({'from': account})
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        logger.info(f"Contract deployed at address: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress

if __name__ == "__main__":
    PROVIDER_URL = os.getenv("WEB3_PROVIDER_URL", "http://localhost:8545")
    CONTRACT_SOURCE = '''
    pragma solidity ^0.8.0;

    contract TestContract {
        uint256 public value;

        function setValue(uint256 _value) public {
            value = _value;
        }
    }
    '''
    
    deployer = Deployer(PROVIDER_URL, CONTRACT_SOURCE)
    deployer.deploy_contract()
