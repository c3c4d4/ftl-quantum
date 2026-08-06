"""Exercise 02 - run the Bell circuit on an IBM Quantum backend.

Set IBM_QUANTUM_TOKEN locally (never commit it).  A local Aer run is available
with ``--local`` so the circuit and its noise-free reference remain testable.
"""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Mapping

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

from exercise_01_entanglement import build_circuit


def run_local(shots: int = 500) -> Mapping[str, int]:
    """Run the identical Bell circuit locally, without pretending it is hardware."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    return AerSimulator().run(build_circuit(), shots=shots).result().get_counts()


def run_on_ibm_quantum(
    shots: int = 500,
    backend_name: str | None = None,
    token: str | None = None,
) -> Mapping[str, int]:
    """Submit the Bell circuit to IBM Quantum using a token from the environment."""
    if shots <= 0:
        raise ValueError("shots must be positive")
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
    except ImportError as exc:
        raise RuntimeError(
            "Install qiskit-ibm-runtime to use hardware execution"
        ) from exc

    service = QiskitRuntimeService(
        channel="ibm_quantum",
        token=token or os.environ.get("IBM_QUANTUM_TOKEN"),
    )
    backend = service.backend(backend_name) if backend_name else service.least_busy(
        simulator=False, operational=True
    )
    circuit = transpile(build_circuit(), backend)
    job = Sampler(mode=backend).run([circuit], shots=shots)
    counts = job.result()[0].data.c.get_counts()
    print(f"Backend: {backend.name}; job: {job.job_id()}")
    return counts


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default=500)
    parser.add_argument("--backend", help="IBM backend name")
    parser.add_argument("--local", action="store_true", help="use Aer instead of hardware")
    parser.add_argument("--output", help="save the histogram to a PNG")
    args = parser.parse_args()
    circuit = build_circuit()
    print(circuit.draw())
    counts = run_local(args.shots) if args.local else run_on_ibm_quantum(args.shots, args.backend)
    print(counts)
    figure = plot_histogram(counts, title="Exercise 02: Bell state on hardware")
    if args.output:
        figure.savefig(args.output, bbox_inches="tight")
    else:
        figure.show()


if __name__ == "__main__":
    main()
