import unittest
from web3 import Web3
from solcx import compile_source

class TestSmartContracts(unittest.TestCase):
    def setUp(self):
        self.w3 = Web3(Web3.EthereumTesterProvider())
        self.contract_source = '''
        pragma solidity ^0.8.0;

        contract TestContract {
            uint256 public value;

            function setValue(uint256 _value) public {
                value = _value;
            }
        }
        '''
        self.contract_interface = self.compile_contract()
        self.contract = self.deploy_contract()

    def compile_contract(self):
        """Compile the smart contract."""
        compiled_sol = compile_source(self.contract_source)
        return compiled_sol['<stdin>:TestContract']

    def deploy_contract(self):
        """Deploy the smart contract."""
        contract = self.w3.eth.contract(abi=self.contract_interface['abi'], bytecode=self.contract_interface['bin'])
        tx_hash = contract.constructor().transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.contract_interface['abi'])

    def test_set_value(self):
        """Test setting a value in the smart contract."""
        tx_hash = self.contract.functions.setValue(42).transact()
        self.w3.eth.waitForTransactionReceipt(tx_hash)

        value = self.contract.functions.value().call()
        self.assertEqual(value, 42)

if __name__ == '__main__':
    unittest.main()
