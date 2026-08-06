"""Exercise 03 - Deutsch-Jozsa for three input qubits (four total qubits)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Mapping

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

OracleBuilder = Callable[[QuantumCircuit, list[int], int], None]


def constant_oracle(value: int = 0) -> OracleBuilder:
    """Return an oracle f(x)=value; the last qubit is the target/ancilla."""
    if value not in (0, 1):
        raise ValueError("constant value must be 0 or 1")

    def apply(circuit: QuantumCircuit, inputs: list[int], ancilla: int) -> None:
        if value:
            circuit.x(ancilla)

    return apply


def balanced_parity_oracle(mask: int) -> OracleBuilder:
    """Return f(x)=parity(x & mask), a balanced oracle for non-zero mask."""
    def apply(circuit: QuantumCircuit, inputs: list[int], ancilla: int) -> None:
        for index, qubit in enumerate(inputs):
            if mask & (1 << index):
                circuit.cx(qubit, ancilla)

    return apply


def build_circuit(oracle: OracleBuilder, input_qubits: int = 3) -> QuantumCircuit:
    """Build a Deutsch-Jozsa circuit; total qubits are input_qubits + one ancilla."""
    if input_qubits < 1:
        raise ValueError("input_qubits must be positive")
    circuit = QuantumCircuit(input_qubits + 1, input_qubits)
    inputs = list(range(input_qubits))
    ancilla = input_qubits
    circuit.x(ancilla)
    circuit.h(ancilla)
    circuit.h(inputs)
    oracle(circuit, inputs, ancilla)
    circuit.h(inputs)
    circuit.measure(inputs, range(input_qubits))
    return circuit


def classify_counts(counts: Mapping[str, int]) -> str:
    """Classify a result: all-zero means constant; any non-zero result is balanced."""
    if not counts:
        raise ValueError("counts cannot be empty")
    return "constant" if set(counts) == {"0" * len(next(iter(counts)))} else "balanced"


def simulate(oracle: OracleBuilder, shots: int = 500) -> Mapping[str, int]:
    if shots <= 0:
        raise ValueError("shots must be positive")
    result = AerSimulator().run(build_circuit(oracle), shots=shots).result()
    return result.get_counts()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--balanced-mask", type=lambda value: int(value, 0))
    parser.add_argument("--shots", type=int, default=500)
    parser.add_argument("--output")
    args = parser.parse_args()
    oracle = balanced_parity_oracle(args.balanced_mask) if args.balanced_mask else constant_oracle()
    circuit = build_circuit(oracle)
    print(circuit.draw())
    counts = simulate(oracle, args.shots)
    print(counts, "=>", classify_counts(counts))
    figure = plot_histogram(counts, title="Exercise 03: Deutsch-Jozsa")
    if args.output:
        figure.savefig(args.output, bbox_inches="tight")
    else:
        figure.show()


if __name__ == "__main__":
    main()
