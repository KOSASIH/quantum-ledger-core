import socket
import threading
import time
import logging
from peer_to_peer import PeerToPeer

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Node:
    def __init__(self, host='localhost', port=5000):
        self.p2p = PeerToPeer(host, port)
        self.p2p.start_server()
        self.connected_nodes = set()  # Track connected nodes
        self.health_check_interval = 10  # Interval for health checks in seconds
        self.node_discovery_interval = 30  # Interval for discovering new nodes

        # Start background threads for health checks and node discovery
        threading.Thread(target=self.health_check_nodes, daemon=True).start()
        threading.Thread(target=self.discover_nodes, daemon=True).start()

    def connect_to(self, address):
        """Connects to another node."""
        self.p2p.connect_to_node(address)
        self.connected_nodes.add(address)

    def send_message(self, message):
        """Sends a message to all connected nodes."""
        self.p2p.broadcast_message(message)

    def health_check_nodes(self):
        """Periodically checks the health of connected nodes."""
        while True:
            for node in list(self.connected_nodes):
                try:
                    # Send a ping message to check if the node is alive
                    ping_message = {'type': 'ping', 'id': f'ping-{time.time()}'}
                    self.p2p.broadcast_message(ping_message)
                    logging.info(f"Sent ping to {node}")
                except Exception as e:
                    logging.error(f"Error checking health of node {node}: {e}")
                    self.connected_nodes.remove(node)  # Remove unresponsive nodes
                    logging.info(f"Removed unresponsive node: {node}")
            time.sleep(self.health_check_interval)

    def discover_nodes(self):
        """Periodically discovers new nodes in the network."""
        while True:
            # Implement a mechanism to discover new nodes (e.g., through a known seed node)
            # For demonstration, we will just log the discovery process
            logging.info("Discovering new nodes...")
            # Here you would implement actual discovery logic
            time.sleep(self.node_discovery_interval)

    def dynamic_configuration(self, new_config):
        """Dynamically updates node configuration."""
        # Update node parameters based on new_config
        logging.info(f"Updating node configuration: {new_config}")
        # Example: self.health_check_interval = new_config.get('health_check_interval', self.health_check_interval)

# Example usage
if __name__ == "__main__":
    node = Node()
    node.connect_to(('localhost', 5001))  # Connect to another node
    node.send_message({'type': 'text', 'content': 'Hello, World!', 'id': 'msg-001'})
