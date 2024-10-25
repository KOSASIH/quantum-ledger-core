from Crypto.Cipher import AES, ChaCha20
from Crypto.Random import get_random_bytes
import base64
import os
import json
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256

class Encryption:
    def __init__(self, key=None):
        self.key = key or get_random_bytes(32)  # AES-256
        self.salt = get_random_bytes(16)  # Salt for key derivation

    def encrypt_aes(self, plaintext):
        """Encrypts plaintext using AES encryption."""
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

    def decrypt_aes(self, ciphertext):
        """Decrypts ciphertext using AES encryption."""
        raw = base64.b64decode(ciphertext.encode())
        nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    def encrypt_chacha20(self, plaintext):
        """Encrypts plaintext using ChaCha20 encryption."""
        cipher = ChaCha20.new(key=self.key)
        ciphertext = cipher.encrypt(plaintext.encode())
        return base64.b64encode(cipher.nonce + ciphertext).decode()

    def decrypt_chacha20(self, ciphertext):
        """Decrypts ciphertext using ChaCha20 encryption."""
        raw = base64.b64decode(ciphertext.encode())
        nonce, ciphertext = raw[:8], raw[8:]
        cipher = ChaCha20.new(nonce=nonce, key=self.key)
        return cipher.decrypt(ciphertext).decode()

    def hybrid_encrypt(self, plaintext):
        """Hybrid encryption using AES and RSA."""
        # Generate a random AES key
        aes_key = get_random_bytes(32)  # AES-256
        aes_cipher = AES.new(aes_key, AES.MODE_GCM)
        ciphertext, tag = aes_cipher.encrypt_and_digest(plaintext.encode())

        # Encrypt the AES key with RSA (placeholder for RSA encryption)
        # In practice, you would use a library like PyCryptodome for RSA
        encrypted_aes_key = self.rsa_encrypt(aes_key)  # Placeholder function

        return {
            'ciphertext': base64.b64encode(aes_cipher.nonce + tag + ciphertext).decode(),
            'encrypted_aes_key': base64.b64encode(encrypted_aes_key).decode()
        }

    def hybrid_decrypt(self, encrypted_data):
        """Decrypts hybrid encrypted data."""
        # Decrypt the AES key with RSA (placeholder for RSA decryption)
        aes_key = self.rsa_decrypt(base64.b64decode(encrypted_data['encrypted_aes_key'].encode()))  # Placeholder function

        # Decrypt the ciphertext using AES
        raw = base64.b64decode(encrypted_data['ciphertext'].encode())
        nonce, tag, ciphertext = raw[:16], raw[16:32], raw[32:]
        aes_cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
        return aes_cipher.decrypt_and_verify(ciphertext, tag).decode()

    def derive_key(self, password):
        """Derives a key from a password using PBKDF2."""
        return PBKDF2(password, self.salt, dkLen=32, count=100000, hmac_hash_module=SHA256)

    def rsa_encrypt(self, data):
        """Placeholder for RSA encryption."""
        # Implement RSA encryption here
        return data  # Replace with actual RSA encrypted data

    def rsa_decrypt(self, data):
        """Placeholder for RSA decryption."""
        # Implement RSA decryption here
        return data  # Replace with actual RSA decrypted data

# Example usage
if __name__ == "__main__":
    encryption = Encryption()
    
    # AES Encryption
    plaintext = "This is a secret message."
    encrypted_aes = encryption.encrypt_aes(plaintext)
    print("AES Encrypted:", encrypted_aes)
    print("AES Decrypted:", encryption.decrypt_aes(encrypted_aes))

    # ChaCha20 Encryption
    encrypted_chacha = encryption.encrypt_chacha20(plaintext)
    print("ChaCha20 Encrypted:", encrypted_chacha)
    print("ChaCha20 Decrypted:", encryption.decrypt_chacha20(encrypted_chacha))

    # Hybrid Encryption
    hybrid_data = encryption.hybrid_encrypt(plaintext)
    print("Hybrid Encrypted:", hybrid_data)
    print("Hybrid Decrypted:", encryption.hybrid_decrypt(hybrid_data))

    # Key Derivation
    password = "my_secret_password"
    derived_key = encryption.derive_key(password)
    print("Derived Key:", derived_key.hex())
