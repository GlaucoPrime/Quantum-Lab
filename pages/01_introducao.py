import streamlit as st
import plotly.graph_objects as go
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

st.header("Módulo 1 — Introdução aos qubits")

st.markdown(
    """
Um **bit clássico** está em `0` ou `1`. Um **qubit** pode estar em uma **superposição**:
`α|0⟩ + β|1⟩`, com `|α|² + |β|² = 1`.

A porta **H** cria uma superposição uniforme a partir de `|0⟩`:
`H|0⟩ = (|0⟩ + |1⟩)/√2`.
"""
)

tab1, tab2 = st.tabs(["Visualização do estado", "Superposição interativa"])

with tab1:
    st.markdown("#### Estado |0⟩ vs. estado após H")
    qc0 = QuantumCircuit(1)
    sv0 = Statevector.from_instruction(qc0)
    qch = QuantumCircuit(1)
    qch.h(0)
    svh = Statevector.from_instruction(qch)

    col1, col2 = st.columns(2)
    with col1:
        st.write("**|0⟩** — amplitudes:", [round(abs(a), 3) for a in sv0.data])
        st.plotly_chart(
            go.Figure(go.Bar(x=["|0⟩", "|1⟩"], y=[abs(a) ** 2 for a in sv0.data])),
            use_container_width=True,
        )
    with col2:
        st.write("**H|0⟩** — amplitudes:", [round(abs(a), 3) for a in svh.data])
        st.plotly_chart(
            go.Figure(go.Bar(x=["|0⟩", "|1⟩"], y=[abs(a) ** 2 for a in svh.data])),
            use_container_width=True,
        )

with tab2:
    st.markdown("#### Ajuste o ângulo θ e veja o estado resultante")
    theta = st.slider("Ângulo θ (graus)", 0, 180, 90)
    import numpy as np
    state = [np.cos(np.radians(theta) / 2), np.sin(np.radians(theta) / 2)]
    probs = [abs(a) ** 2 for a in state]
    st.plotly_chart(
        go.Figure(go.Bar(x=["|0⟩", "|1⟩"], y=probs, text=[f"{p:.2%}" for p in probs])),
        use_container_width=True,
    )
    st.caption(f"P(|0⟩) = {probs[0]:.2%} | P(|1⟩) = {probs[1]:.2%}")