import streamlit as st
from modules.quantum_engine import build_gate_demo, run_circuit
from modules.export_utils import counts_to_csv, plotly_to_png
import plotly.graph_objects as go

st.header("Módulo 2 — Laboratório de portas quânticas")

GATE_INFO = {
    "X": "Inverte o estado: X|0⟩ = |1⟩ e X|1⟩ = |0⟩. É o NOT quântico.",
    "H": "Cria superposição: H|0⟩ = (|0⟩ + |1⟩)/√2. Fundamental para paralelismo quântico.",
    "Z": "Altera a fase: Z|1⟩ = −|1⟩. Não muda probabilidades imediatamente, mas afeta interferências.",
    "CNOT": "Controla a inversão: inverte o alvo somente se o controle for |1⟩. Base do emaranhamento.",
}

gate = st.selectbox("Escolha a porta", list(GATE_INFO))
st.info(GATE_INFO[gate])

num_qubits = 2 if gate == "CNOT" else 1
shots = st.select_slider("Número de medições", [100, 500, 1000, 5000], value=1000)

if st.button("Executar experimento", type="primary"):
    try:
        qc = build_gate_demo(gate, qubits=num_qubits)
        result = run_circuit(qc, shots=shots, seed=42)
        counts = result["counts"]

        st.subheader("Circuito executado")
        st.text(qc.draw(output="text"))

        st.subheader("Resultados")
        fig = go.Figure(go.Bar(x=list(counts.keys()), y=list(counts.values())))
        fig.update_layout(xaxis_title="Estado", yaxis_title="Contagem")
        st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("Baixar CSV", counts_to_csv(counts), "porta.csv", "text/csv")
        with col2:
            st.download_button("Baixar PNG", plotly_to_png(fig), "porta.png", "image/png")
    except Exception as e:
        st.error(f"Erro na execução: {e}")