import os
import json
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidToken

class KeyManagement:
    def __init__(self, key_file='keys.json'):
        self.key_file = key_file
        self.keys = {}
        self.load_keys()

    def generate_rsa_key_pair(self):
        """Generates an RSA key pair."""
        key = RSA.generate(2048)
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        return private_key, public_key

    def save_key_pair(self, alias):
        """Saves an RSA key pair to the key store."""
        private_key, public_key = self.generate_rsa_key_pair()
        self.keys[alias] = {
            'private_key': private_key.decode(),
            'public_key': public_key.decode()
        }
        self.save_keys()

    def load_keys(self):
        """Loads keys from the key store."""
        if os.path.exists(self.key_file):
            with open(self.key_file, 'r') as file:
                self.keys = json.load(file)

    def save_keys(self):
        """Saves keys to the key store."""
        with open(self.key_file, 'w') as file:
            json.dump(self.keys, file)

    def get_public_key(self, alias):
        """Retrieves the public key for a given alias."""
        return self.keys.get(alias, {}).get('public_key')

    def get_private_key(self, alias):
        """Retrieves the private key for a given alias."""
        return self.keys.get(alias, {}).get('private_key')

    def generate_symmetric_key(self):
        """Generates a random symmetric key."""
        return get_random_bytes(32)  # AES-256

    def encrypt_key(self, key, password):
        """Encrypts a symmetric key using a password."""
        salt = get_random_bytes(16)
        derived_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        fernet = Fernet(Fernet.generate_key())
        encrypted_key = fernet.encrypt(key)
        return {
            'encrypted_key': encrypted_key.decode(),
            'salt': base64.b64encode(salt).decode()
        }

    def decrypt_key(self, encrypted_data, password):
        """Decrypts a symmetric key using a password."""
        encrypted_key = encrypted_data['encrypted_key'].encode()
        salt = base64.b64decode(encrypted_data['salt'].encode())
        derived_key = PBKDF2(password, salt, dkLen=32, count=100000, hmac_hash_module=SHA256)
        fernet = Fernet(Fernet.generate_key())
        try:
            return fernet.decrypt(encrypted_key)
        except InvalidToken:
            raise ValueError("Invalid password or corrupted key.")

    def rotate_key(self, alias):
        """Rotates the key for a given alias."""
        if alias in self.keys:
            self.save_key_pair(alias)  # Generate and save a new key pair
            print(f"Key for {alias} has been rotated.")
        else:
            print(f"No key found for alias: {alias}")

    def delete_key(self, alias):
        """Deletes a key for a given alias."""
        if alias in self.keys:
            del self.keys[alias]
            self.save_keys()
            print(f"Key for {alias} has been deleted.")
        else:
            print(f"No key found for alias: {alias}")

# Example usage
if __name__ == "__main__":
    km = KeyManagement()
    
    # Generate and save RSA key pair
    km.save_key_pair('user1')
    print("Public Key:", km.get_public_key('user1'))
    
    # Generate a symmetric key
    symmetric_key = km.generate_symmetric_key()
    print("Symmetric Key:", symmetric_key.hex())
    
    # Encrypt the symmetric key
    password = "my_secure_password"
    encrypted_data = km.encrypt_key(symmetric_key, password)
    print("Encrypted Symmetric Key:", encrypted_data)
    
    # Decrypt the symmetric key
    decrypted_key = km.decrypt_key(encrypted_data, password)
    print("Decrypted Symmetric Key:", decrypted_key.hex())
    
    # Rotate the key
    km.rotate_key('user1')
 # Delete the key
    km.delete_key('user1')
