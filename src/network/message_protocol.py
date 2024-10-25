import json
import hashlib
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidToken

class MessageProtocol:
    def __init__(self):
        self.handlers = {
            'text': self.handle_text_message,
            'ping': self.handle_ping,
            'ack': self.handle_acknowledgment,
            # Add more message types as needed
        }
        self.secret_key = Fernet.generate_key()  # Generate a key for encryption
        self.fernet = Fernet(self.secret_key)

    def process_message(self, message, peer):
        """Processes incoming messages based on their type."""
        message_type = message.get('type')
        if self.verify_integrity(message):
            handler = self.handlers.get(message_type)
            if handler:
                handler(message, peer)
            else:
                print(f"Unknown message type: {message_type}")
        else:
            print("Message integrity check failed.")

    def handle_text_message(self, message, peer):
        """Handles text messages."""
        print(f"Text message received: {message['content']}")
        # Send acknowledgment
        ack_message = {'type': 'ack', 'id': message['id']}
        peer.broadcast_message(ack_message)

    def handle_ping(self, message, peer):
        """Handles ping messages for node availability."""
        print("Ping received, responding with pong.")
        pong_message = {'type': 'pong', 'id': message['id']}
        peer.broadcast_message(pong_message)

    def handle_acknowledgment(self, message, peer):
        """Handles acknowledgment messages."""
        print(f"Acknowledgment received for message ID: {message['id']}")

    def encrypt_message(self, message):
        """Encrypts a message for confidentiality."""
        message_json = json.dumps(message).encode()
        encrypted_message = self.fernet.encrypt(message_json)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        """Decrypts a message."""
        try:
            decrypted_message = self.fernet.decrypt(encrypted_message)
            return json.loads(decrypted_message.decode())
        except InvalidToken:
            print("Failed to decrypt message.")
            return None

    def verify_integrity(self, message):
        """Verifies the integrity of a message using a hash."""
        message_id = message.get('id')
        message_content = json.dumps(message, sort_keys=True).encode()
        hash_value = hashlib.sha256(message_content).hexdigest()
        return hash_value == message.get('hash')

    def sign_message(self, message, private_key):
        """Signs a message using the private key."""
        message_bytes = json.dumps(message).encode()
        signature = private_key.sign(
            message_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        message['signature'] = signature.hex()  # Store signature in hex format

    def verify_signature(self, message, public_key):
        """Verifies the signature of a message."""
        signature = bytes.fromhex(message.pop('signature'))
        message_bytes = json.dumps(message).encode()
        try:
            public_key.verify(
                signature,
                message_bytes,
                padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Signature verification failed: {e}")
            return False

# Example usage
if __name__ == "__main__":
    protocol = MessageProtocol()
    text_message = {
        'type': 'text',
        'content': 'Hello, World!',
        'id': 'msg-001',
        'hash': '',  # Placeholder for hash
    }
    # Calculate and set the hash for integrity check
    text_message['hash'] = hashlib.sha256(json.dumps(text_message, sort_keys=True).encode()).hexdigest()
    
    encrypted_message = protocol.encrypt_message(text_message)
    print("Encrypted Message:", encrypted_message)

    decrypted_message = protocol.decrypt_message(encrypted_message)
    print("Decrypted Message:", decrypted_message)
