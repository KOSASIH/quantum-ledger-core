# Getting Started with Quantum Ledger

## Introduction
Welcome to the Quantum Ledger Getting Started guide! This tutorial will walk you through the initial setup and basic usage of the Quantum Ledger system, enabling you to create and manage transactions seamlessly.

## Prerequisites
Before you begin, ensure you have the following:
- A basic understanding of blockchain technology.
- Python 3.x installed on your machine.
- An API key for accessing the Quantum Ledger API.

## Step 1: Clone the Repository
Start by cloning the Quantum Ledger repository to your local machine:

```bash
git clone https://github.com/KOSASIH/quantum-ledger-core.git
cd quantum-ledger-core
```

## Step 2: Install Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Step 3: Configure Your Environment
Create a configuration file named config.py in the root directory of the project. Add your API key and the node URL:

```python
API_KEY = "YOUR_API_KEY"
NODE_URL = "https://api.quantum-ledger-core.com/v1"
```

## Step 4: Create Your First Transaction
You can create a transaction using the provided API. Here’s a simple example:

```python
from quantum_ledger_core import create_transaction

# Define transaction details
transaction = create_transaction(
    from_address="0x1234567890abcdef",
    to_address="0xfedcba9876543210",
    amount=10.0,
    currency="QLD",
    metadata={"message": "First transaction!"}
)

print(f"Transaction ID: {transaction.transaction_id}")
```

## Step 5: Check Transaction Status

After creating a transaction, you can check its status:

```python
from quantum_ledger_core import get_transaction_status

transaction_id = transaction.transaction_id
status = get_transaction_status(transaction_id=transaction_id)

print(f"Transaction Status: {status.status}")
```

# Conclusion
Congratulations! You have successfully set up the Quantum Ledger environment and created your first transaction. For more advanced features and functionalities, please refer to the advanced_usage.md tutorial.
