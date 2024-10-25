# Quantum Ledger API Reference

## Introduction
The Quantum Ledger API provides a set of endpoints for interacting with the Quantum Ledger system. This document outlines the available API endpoints, their parameters, and response formats.

## Base URL

https://api.quantum-ledger-core.com/v1


## Authentication
All API requests require an API key for authentication. Include the API key in the request header as follows:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### 1. Create Transaction
- **Endpoint**: `/transactions`
- **Method**: `POST`
- **Description**: Initiates a new transaction.
- **Request Body**:
    ```json
    {
        "from": "string",
        "to": "string",
        "amount": "number",
        "currency": "string",
        "metadata": "object"
    }
    ```
- **Response**:
    - **201 Created**: Transaction successfully created.
    - **400 Bad Request**: Invalid input data.

### 2. Get Transaction Status
- **Endpoint**: `/transactions/{transaction_id}`
- **Method**: `GET`
- **Description**: Retrieves the status of a specific transaction.
- **Parameters**:
    - `transaction_id` (path): The ID of the transaction.
- **Response**:
    - **200 OK**: Returns transaction details.
    - **404 Not Found**: Transaction not found.

### 3. Get Ledger State
- **Endpoint**: `/ledger`
- **Method**: `GET`
- **Description**: Retrieves the current state of the ledger.
- **Response**:
    - **200 OK**: Returns the current ledger state.

## Conclusion
The Quantum Ledger API provides a robust interface for developers to interact with the system. For further details on each endpoint, please refer to the specific sections in this document.
