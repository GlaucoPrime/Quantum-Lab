"""
Quantum Lab — ponto de entrada.
"""
import streamlit as st
from modules.qr_access import build_access_url, generate_qr_image, get_local_ip

st.set_page_config(
    page_title="Quantum Lab",
    page_icon="⚛️",
    layout="wide",
)

# --- barra lateral: QR Code de acesso ---
with st.sidebar:
    st.markdown("### 📱 Acesse pelo celular")
    port = st.number_input("Porta do servidor", min_value=1024, max_value=65535, value=8501)
    url = build_access_url(int(port))
    st.code(url, language="text")
    st.image(generate_qr_image(url), caption="Escaneie para abrir no celular", width=200)
    st.caption("Dispositivos na mesma rede Wi‑Fi. Não use localhost no celular.")

# --- conteúdo principal ---
st.title("⚛️ Quantum Lab")
st.subheader("Laboratório interativo de computação quântica")

st.markdown(
    """
Bem‑vindo ao **Quantum Lab**. Aqui você pode explorar os fundamentos da computação quântica
sem precisar escrever código:

- **Introdução aos qubits** — entenda bits, qubits e superposição.
- **Portas quânticas** — experimente X, H, Z e CNOT com explicações didáticas.
- **Construtor de circuitos** — monte sequências de portas e execute no simulador.
- **Emaranhamento** — crie estados de Bell e veja correlações reais.
- **Medição quântica** — compare poucas e muitas medições com histogramas.

Use o menu lateral para navegar entre os módulos. Todos os resultados vêm de **simulação real com Qiskit Aer**.
"""
)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Qubits suportados", "1 – 5")
with col2:
    st.metric("Simulador", "Qiskit Aer")
with col3:
    st.metric("Medições disponíveis", "100 – 5.000")

st.info(
    "Para executar corretamente, inicie o servidor com "
    "`streamlit run app.py --server.address 0.0.0.0 --server.port 8501`. "
    "O QR Code ao lado já aponta para o endereço de rede correto."
)