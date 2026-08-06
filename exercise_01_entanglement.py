"""Exercise 01 - create and measure the Bell state (|00> + |11>) / sqrt(2)."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Mapping

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def build_circuit() -> QuantumCircuit:
    """Return a two-qubit Bell-state circuit with measurements."""
    circuit = QuantumCircuit(2, 2)
    circuit.h(0)
    circuit.cx(0, 1)
    circuit.measure([0, 1], [0, 1])
    return circuit


def simulate(shots: int = 500) -> Mapping[str, int]:
    if shots <= 0:
        raise ValueError("shots must be positive")
    result = AerSimulator().run(build_circuit(), shots=shots).result()
    return result.get_counts()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default=500)
    parser.add_argument("--output", help="save the histogram to a PNG")
    args = parser.parse_args()
    print(build_circuit().draw())
    counts = simulate(args.shots)
    print(counts)
    figure = plot_histogram(counts, title="Exercise 01: entanglement")
    if args.output:
        figure.savefig(args.output, bbox_inches="tight")
    else:
        figure.show()


if __name__ == "__main__":
    main()
