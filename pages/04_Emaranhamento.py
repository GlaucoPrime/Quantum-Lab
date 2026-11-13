import streamlit as st
from modules.quantum_engine import build_bell_circuit, run_circuit
from modules.export_utils import counts_to_csv, plotly_to_png
import plotly.graph_objects as go

st.header("Módulo 4 — Emaranhamento")

st.markdown(
    """
O estado de Bell `(|00⟩ + |11⟩)/√2` é criado com **H** no qubit 0 e **CNOT(0→1)**.
Os resultados são perfeitamente correlacionados: se o qubit 0 for medido como `0`, o qubit 1 também será `0`; se for `1`, o qubit 1 também será `1`.
"""
)

shots = st.select_slider("Número de medições", [100, 500, 1000, 5000], value=1000)

if st.button("Executar estado de Bell", type="primary"):
    try:
        qc = build_bell_circuit()
        result = run_circuit(qc, shots=shots, seed=123)
        counts = result["counts"]

        st.text(qc.draw(output="text"))

        # separa correlação
        corr = {"00": counts.get("00", 0), "01": counts.get("01", 0),
                "10": counts.get("10", 0), "11": counts.get("11", 0)}

        fig = go.Figure(go.Bar(x=list(corr), y=list(corr.values())))
        fig.update_layout(xaxis_title="Estado dos dois qubits", yaxis_title="Contagem")
        st.plotly_chart(fig, use_container_width=True)

        total = sum(corr.values()) or 1
        st.write(
            f"Correlação observada: **{100*(corr['00']+corr['11'])/total:.1f}%** dos resultados "
            "foram `00` ou `11`."
        )

        st.download_button("CSV", counts_to_csv(corr), "bell.csv")
        st.download_button("PNG", plotly_to_png(fig), "bell.png")
    except Exception as e:
        st.error(f"Erro: {e}")