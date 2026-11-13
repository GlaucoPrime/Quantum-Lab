"""
Motor quântico do Quantum Lab.
Usa Qiskit 2.x + Qiskit Aer para simulação local.
"""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector


def _simulator(seed: int | None = None) -> AerSimulator:
    """Cria um simulador Aer com seed opcional para reprodutibilidade."""
    return AerSimulator(seed_simulator=seed)


def run_circuit(circuit: QuantumCircuit, shots: int = 1024, seed: int | None = None) -> dict:
    """
    Executa um circuito no AerSimulator e retorna contagens.
    Levanta ValueError se o circuito estiver vazio.
    """
    # Qiskit 2.x: 'num_instructions' não existe mais; use 'size()'
    if circuit.size() == 0:
        raise ValueError("O circuito está vazio. Adicione pelo menos uma porta.")

    sim = _simulator(seed)
    compiled = transpile(circuit, sim)
    result = sim.run(compiled, shots=shots).result()
    counts = result.get_counts()

    # normaliza chaves: Qiskit pode retornar '0x0' em circuitos sem medição explícita
    normalized = {}
    for key, value in counts.items():
        clean_key = key.replace("0x", "").replace(" ", "")
        normalized[clean_key] = normalized.get(clean_key, 0) + value

    return {
        "counts": normalized,
        "shots": shots,
        "depth": circuit.depth(),
        "size": circuit.size(),   # também trocado aqui por segurança
    }


def statevector(circuit: QuantumCircuit) -> Statevector:
    """Retorna o vetor de estado final (sem medição) para fins didáticos."""
    return Statevector.from_instruction(circuit)


def build_bell_circuit() -> QuantumCircuit:
    """Circuito de Bell: H no qubit 0, CNOT(0→1)."""
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def build_gate_demo(gate: str, qubits: int = 1) -> QuantumCircuit:
    """
    Constrói um circuito de demonstração para uma porta específica.
    Suporta: 'X', 'H', 'Z', 'CNOT'.
    """
    gate = gate.upper().strip()
    qc = QuantumCircuit(qubits, qubits)

    if gate == "X":
        qc.x(0)
    elif gate == "H":
        qc.h(0)
    elif gate == "Z":
        qc.h(0)          # cria superposição primeiro para a fase ser observável
        qc.z(0)
        qc.h(0)          # volta à base computacional
    elif gate == "CNOT":
        if qubits < 2:
            raise ValueError("CNOT requer pelo menos 2 qubits.")
        qc.h(0)          # superposição no controle para tornar o efeito visível
        qc.cx(0, 1)
    else:
        raise ValueError(f"Porta desconhecida: {gate}")

    qc.measure(range(qubits), range(qubits))
    return qc


def build_user_circuit(num_qubits: int, operations: list[dict]) -> QuantumCircuit:
    """
    Constrói circuito a partir de uma lista de operações.
    Cada operação: {"gate": "h"|"x"|"z"|"cx", "qubits": [0] ou [0,1]}
    """
    qc = QuantumCircuit(num_qubits, num_qubits)
    for op in operations:
        gate = op["gate"].lower()
        qubits = op["qubits"]
        if gate in {"x", "h", "z"}:
            getattr(qc, gate)(qubits[0])
        elif gate == "cx":
            if len(qubits) != 2:
                raise ValueError("CNOT requer dois qubits.")
            qc.cx(qubits[0], qubits[1])
        else:
            raise ValueError(f"Porta não suportada: {gate}")
    qc.measure(range(num_qubits), range(num_qubits))
    return qc