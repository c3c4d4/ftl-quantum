from exercise_00_superposition import build_circuit as superposition_circuit, simulate as superposition
from exercise_01_entanglement import build_circuit as bell_circuit, simulate as bell
from exercise_03_deutsch_jozsa import (
    balanced_parity_oracle,
    classify_counts,
    constant_oracle,
    simulate as deutsch_jozsa,
)
from exercise_04_search import build_circuit as grover_circuit, make_phase_oracle, simulate as grover


def test_superposition_has_one_qubit_and_both_outcomes():
    assert superposition_circuit().num_qubits == 1
    counts = superposition(500)
    assert set(counts) == {"0", "1"}


def test_bell_state_only_contains_correlated_results():
    assert bell_circuit().num_qubits == 2
    assert set(bell(500)) <= {"00", "11"}


def test_deutsch_jozsa_classifies_constant_and_balanced_oracles():
    constant_counts = deutsch_jozsa(constant_oracle(), 100)
    balanced_counts = deutsch_jozsa(balanced_parity_oracle(0b101), 100)
    assert classify_counts(constant_counts) == "constant"
    assert classify_counts(balanced_counts) == "balanced"


def test_grover_finds_marked_state():
    oracle = make_phase_oracle(3, {5})
    counts = grover(oracle, 500)
    assert counts.get("101", 0) > 400
    assert grover_circuit(oracle).num_qubits == 3


def test_invalid_inputs_are_rejected():
    import pytest

    with pytest.raises(ValueError):
        superposition(0)
    with pytest.raises(ValueError):
        make_phase_oracle(1, {0})
