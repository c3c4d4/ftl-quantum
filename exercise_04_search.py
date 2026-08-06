"""Exercise 04 - general Grover search with an explicit oracle and diffuser."""

from __future__ import annotations

import argparse
import math
import sys
from collections.abc import Mapping

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def _phase_flip_all_ones(circuit: QuantumCircuit) -> None:
    target = circuit.num_qubits - 1
    controls = list(range(target))
    if controls:
        circuit.h(target)
        circuit.mcx(controls, target)
        circuit.h(target)
    else:
        circuit.z(target)


def make_phase_oracle(n_qubits: int, marked_states: set[int]) -> QuantumCircuit:
    """Create a phase oracle that flips exactly the supplied basis-state integers."""
    if n_qubits < 2:
        raise ValueError("Grover search requires at least 2 qubits")
    limit = 2**n_qubits
    if not marked_states or any(state < 0 or state >= limit for state in marked_states):
        raise ValueError("marked_states must be non-empty and within the search space")
    oracle = QuantumCircuit(n_qubits, name="Oracle")
    for state in marked_states:
        for qubit in range(n_qubits):
            if not (state >> qubit) & 1:
                oracle.x(qubit)
        _phase_flip_all_ones(oracle)
        for qubit in range(n_qubits):
            if not (state >> qubit) & 1:
                oracle.x(qubit)
    return oracle


def diffuser(n_qubits: int) -> QuantumCircuit:
    """Return the inversion-about-the-mean circuit."""
    circuit = QuantumCircuit(n_qubits, name="Diffuser")
    circuit.h(range(n_qubits))
    circuit.x(range(n_qubits))
    _phase_flip_all_ones(circuit)
    circuit.x(range(n_qubits))
    circuit.h(range(n_qubits))
    return circuit


def build_circuit(oracle: QuantumCircuit, iterations: int | None = None) -> QuantumCircuit:
    """Build Grover's algorithm around any n-qubit phase oracle."""
    n_qubits = oracle.num_qubits
    if n_qubits < 2 or oracle.num_clbits:
        raise ValueError("oracle must have at least 2 qubits and no classical bits")
    if iterations is None:
        iterations = max(1, round(math.pi / 4 * math.sqrt(2**n_qubits)))
    if iterations < 1:
        raise ValueError("iterations must be positive")
    circuit = QuantumCircuit(n_qubits, n_qubits)
    circuit.h(range(n_qubits))
    for _ in range(iterations):
        circuit.compose(oracle, inplace=True)
        circuit.compose(diffuser(n_qubits), inplace=True)
    circuit.measure(range(n_qubits), range(n_qubits))
    return circuit


def simulate(oracle: QuantumCircuit, shots: int = 500, iterations: int | None = None) -> Mapping[str, int]:
    if shots <= 0:
        raise ValueError("shots must be positive")
    return AerSimulator().run(build_circuit(oracle, iterations), shots=shots).result().get_counts()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("n_qubits", type=int)
    parser.add_argument("marked", nargs="+", type=lambda value: int(value, 0))
    parser.add_argument("--shots", type=int, default=500)
    parser.add_argument("--iterations", type=int)
    parser.add_argument("--output")
    args = parser.parse_args()
    oracle = make_phase_oracle(args.n_qubits, set(args.marked))
    circuit = build_circuit(oracle, args.iterations)
    print(circuit.draw())
    counts = simulate(oracle, args.shots, args.iterations)
    print(counts)
    figure = plot_histogram(counts, title="Exercise 04: Grover search")
    if args.output:
        figure.savefig(args.output, bbox_inches="tight")
    else:
        figure.show()


if __name__ == "__main__":
    main()
