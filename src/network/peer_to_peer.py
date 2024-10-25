import socket
import threading
import json
import ssl
import time
import logging
from message_protocol import MessageProtocol
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PeerToPeer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.nodes = set()  # Set of connected nodes
        self.protocol = MessageProtocol()
        self.private_key, self.public_key = self.generate_key_pair()

    def generate_key_pair(self):
        """Generates an RSA key pair for signing messages."""
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        public_key = private_key.public_key()
        return private_key, public_key

    def start_server(self):
        """Starts the P2P server to listen for incoming connections."""
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

    def run_server(self):
        """Runs the server to accept incoming connections."""
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.load_cert_chain(certfile='server.crt', keyfile='server.key')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            logging.info(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                logging.info(f"Connection from {addr}")
                secure_socket = context.wrap_socket(client_socket, server_side=True)
                threading.Thread(target=self.handle_client, args=(secure_socket,)).start()

    def handle_client(self, client_socket):
        """Handles communication with a connected client."""
        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode())
                self.protocol.process_message(message, self)

    def connect_to_node(self, node_address):
        """Connects to another node in the network."""
        context = ssl.create_default_context()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(node_address)
            secure_socket = context.wrap_socket(client_socket, server_hostname=node_address[0])
            self.nodes.add(node_address)
            logging.info(f"Connected to node: {node_address}")

    def broadcast_message(self, message):
        """Broadcasts a message to all connected nodes."""
        for node in self.nodes:
            try:
                context = ssl.create_default_context()
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                    client_socket.connect(node)
                    secure_socket = context.wrap_socket(client_socket, server_hostname=node[0])
                    secure_socket.sendall(json.dumps(message).encode())
            except Exception as e:
                logging.error(f"Failed to send message to {node}: {e}")

    def sign_message(self, message):
        """Signs a message using the private key."""
        message_bytes = json.dumps(message).encode()
        signature = self.private_key.sign(
            message_bytes,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, message, signature, public_key):
        """Verifies the signature of a message."""
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
            logging.error(f"Signature verification failed: {e}")
            return False

# Example usage
if __name__ == "__main__":
    p 2p = PeerToPeer()
    p2p.start_server()
    time.sleep(1)  # Allow server to start
    p2p.connect_to_node(('localhost', 5001))  # Example of connecting to another node
