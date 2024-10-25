import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble, execute
from qiskit.visualization import plot_histogram
import random

class QuantumCryptography:
    def __init__(self):
        self.backend = Aer.get_backend('qasm_simulator')

    def generate_quantum_key(self, num_qubits=1):
        """Generates a quantum key using superposition."""
        qc = QuantumCircuit(num_qubits, num_qubits)
        qc.h(range(num_qubits))  # Apply Hadamard gate to create superposition
        qc.measure(range(num_qubits), range(num_qubits))  # Measure the qubits

        # Execute the circuit
        transpiled_qc = transpile(qc, self.backend)
        qobj = assemble(transpiled_qc)
        result = execute(qc, self.backend).result()
        counts = result.get_counts(qc)
        return self._extract_key_from_counts(counts)

    def _extract_key_from_counts(self, counts):
        """Extracts a binary key from the measurement counts."""
        return ''.join(sorted(counts, key=counts.get, reverse=True)[0])  # Most frequent outcome

    def quantum_key_distribution(self, sender_key, receiver_key):
        """Simulates a simple quantum key distribution protocol."""
        shared_key = self._combine_keys(sender_key, receiver_key)
        return shared_key

    def _combine_keys(self, key1, key2):
        """Combines two keys using XOR operation."""
        combined_key = ''.join(str(int(a) ^ int(b)) for a, b in zip(key1, key2))
        return combined_key

    def bb84_protocol(self, num_bits=8):
        """Implements the BB84 Quantum Key Distribution protocol."""
        # Step 1: Alice prepares a random string of bits and random bases
        alice_bits = np.random.randint(2, size=num_bits)
        alice_bases = np.random.randint(2, size=num_bits)

        # Step 2: Alice sends qubits to Bob
        bob_bases = np.random.randint(2, size=num_bits)
        bob_bits = []

        for i in range(num_bits):
            qc = QuantumCircuit(1, 1)
            if alice_bases[i] == 0:  # Z-basis
                if alice_bits[i] == 1:
                    qc.x(0)  # Prepare |1>
            else:  # X-basis
                if alice_bits[i] == 1:
                    qc.h(0)  # Prepare |+>

            qc.measure(0, 0)
            result = execute(qc, self.backend).result()
            bob_bits.append(result.get_counts(qc).most_frequent())

        # Step 3: Alice and Bob compare bases and keep only the bits where they used the same basis
        key = ''.join([str(bob_bits[i]) for i in range(num_bits) if alice_bases[i] == bob_bases[i]])
        return key

    def entanglement_based_cryptography(self):
        """Simulates entanglement-based quantum key distribution."""
        # Create entangled qubits
        qc = QuantumCircuit(2)
        qc.h(0)
        qc.cx(0, 1)
        qc.measure_all()

        # Execute the circuit
        result = execute(qc, self.backend).result()
        counts = result.get_counts(qc)
        return counts

    def post_quantum_key_exchange(self, private_key):
        """Simulates a post-quantum key exchange using lattice-based cryptography."""
        # This is a placeholder for a more complex implementation
        # In practice, you would use a library like NTRU or Kyber
        return f"Post-quantum key derived from {private_key}"

# Example usage
if __name__ == "__main__":
    qc = QuantumCryptography()
    print("Quantum Key:", qc.generate_quantum_key(5))
    print("BB84 Key:", qc.bb84_protocol(8))
    print("Entanglement Counts:", qc.entanglement_based_cryptography())
