import streamlit as st
from modules.quantum_engine import build_user_circuit, run_circuit
from modules.export_utils import counts_to_csv, plotly_to_png
import plotly.graph_objects as go

st.header("Módulo 3 — Construtor de circuitos")

num_qubits = st.slider("Número de qubits", 1, 5, 2)

# estado do circuito na sessão (isolado por usuário)
if "construtor_ops" not in st.session_state:
    st.session_state.construtor_ops = []

with st.form("add_op"):
    col1, col2, col3 = st.columns(3)
    with col1:
        gate = st.selectbox("Porta", ["H", "X", "Z", "CNOT"])
    with col2:
        q1 = st.number_input("Qubit alvo/controle", 0, num_qubits - 1, 0)
    with col3:
        q2 = st.number_input("Qubit alvo (CNOT)", 0, num_qubits - 1, min(1, num_qubits - 1))
    submitted = st.form_submit_button("Adicionar porta")
    if submitted:
        qubits = [int(q1), int(q2)] if gate == "CNOT" else [int(q1)]
        st.session_state.construtor_ops.append({"gate": gate.lower(), "qubits": qubits})

st.write("**Sequência atual:**", st.session_state.construtor_ops or "vazia")

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Limpar circuito"):
        st.session_state.construtor_ops = []
        st.rerun()
with col_b:
    if st.button("Executar circuito", type="primary"):
        if not st.session_state.construtor_ops:
            st.warning("Adicione pelo menos uma porta.")
        else:
            try:
                qc = build_user_circuit(num_qubits, st.session_state.construtor_ops)
                result = run_circuit(qc, shots=2048, seed=7)
                counts = result["counts"]
                st.text(qc.draw(output="text"))
                fig = go.Figure(go.Bar(x=list(counts), y=list(counts.values())))
                st.plotly_chart(fig, use_container_width=True)
                st.download_button("CSV", counts_to_csv(counts), "construtor.csv")
                st.download_button("PNG", plotly_to_png(fig), "construtor.png")
            except Exception as e:
                st.error(f"Erro: {e}")