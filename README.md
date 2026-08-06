# FTL Quantum

An educational Qiskit implementation of the mandatory exercises from the 42 Ftl_quantum subject. It builds the circuits explicitly so the gates, state preparation, oracle, and diffuser can be inspected during a defense.

## Setup

Python 3.10 or newer is recommended. Create an isolated environment and install the dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

No credentials are needed for exercises 00, 01, 03, or 04. Exercise 02 hardware execution requires an IBM Quantum account and a local environment variable. Never put the token in this repository:

```powershell
$env:IBM_QUANTUM_TOKEN = "your-token"
python exercise_02_quantum_noise.py --backend ibm_brisbane --shots 500
```

The `--local` option runs the same Bell circuit on Aer and is useful for checking the program without cloud access. Hardware results are expected to differ because real devices introduce gate, readout, and decoherence noise.

## Exercises

Each mandatory exercise is a separate Python file, as requested by the subject.

```bash
python exercise_00_superposition.py --shots 500 --output exercise-00.png
python exercise_01_entanglement.py --shots 500 --output exercise-01.png
python exercise_02_quantum_noise.py --shots 500 --backend YOUR_BACKEND --output exercise-02.png
python exercise_03_deutsch_jozsa.py --shots 500 --balanced-mask 0b101
python exercise_04_search.py 3 5 --shots 500
```

Exercise 03 uses four total qubits: three input qubits and one ancilla. `constant_oracle()` and `balanced_parity_oracle()` are small examples for learning; `build_circuit()` accepts any evaluator-supplied oracle function with signature `(circuit, input_qubits, ancilla)`.

Exercise 04 accepts any phase oracle represented by an `n`-qubit `QuantumCircuit`. `make_phase_oracle()` is a transparent example that marks one or more integer basis states. The integers use normal binary labels: for example, state `5` in a 3-qubit search is displayed as `101`. `build_circuit()` performs uniform initialization, repeated oracle/diffuser iterations, and measurement without calling a search algorithm from a library.

## Tests

Run the deterministic simulator checks with:

```bash
pytest -q
```

The tests check the required state correlations, Deutsch-Jozsa classification, Grover success probability, circuit sizes, and invalid-input handling. The hardware path is intentionally not run automatically: it needs a real account, a chosen backend, network access, and incurs queue/runtime costs.

## Implementation notes and limitations

- Aer is used for local simulation; sampling is stochastic, so tests assert physical properties and a conservative Grover success threshold rather than exact counts.
- A Deutsch-Jozsa oracle must be promised to be either constant or balanced. The algorithm's classification is not meaningful for an arbitrary non-promised function.
- Grover's default iteration count is tuned for a single marked item. When the number of marked items is known, pass an appropriate `iterations` value to avoid over-rotation.
- IBM Runtime API availability and backend names can change. Install the pinned dependency range, choose an operational backend available to your account, and keep credentials outside Git.
