import streamlit as st
from modules.quantum_engine import build_gate_demo, run_circuit
from modules.export_utils import counts_to_csv, plotly_to_png, build_report
import plotly.graph_objects as go

st.header("Módulo 5 — Medição quântica")

st.markdown(
    """
Uma **medição individual** colapsa o estado e retorna apenas um resultado.
Repetir o experimento muitas vezes revela a **distribuição de probabilidades**.
Abaixo, o mesmo circuito (H) é executado com diferentes números de medições.
"""
)

shots = st.select_slider("Número de medições", [100, 500, 1000, 5000], value=1000)

if st.button("Executar medição", type="primary"):
    try:
        qc = build_gate_demo("H", qubits=1)
        result = run_circuit(qc, shots=shots, seed=99)
        counts = result["counts"]

        fig = go.Figure(go.Bar(x=list(counts), y=list(counts.values())))
        fig.update_layout(xaxis_title="Estado", yaxis_title="Contagem")
        st.plotly_chart(fig, use_container_width=True)

        total = sum(counts.values())
        for state, count in counts.items():
            st.write(f"- `{state}`: {count} vezes ({100*count/total:.1f}%)")

        report = build_report("Medição quântica", result, counts, extra={"Medições": shots})
        st.download_button("CSV", counts_to_csv(counts), "medicao.csv")
        st.download_button("PNG", plotly_to_png(fig), "medicao.png")
        st.download_button("Relatório (.txt)", report.encode("utf-8"), "relatorio.txt")
    except Exception as e:
        st.error(f"Erro: {e}")