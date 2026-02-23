import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Amorim & Souza Advogados", layout="centered")

# --- ESTILIZAÇÃO UI/UX ---
st.markdown("""
    <style>
    .stApp { background-color: #f8fbff; }
    .nome-cliente { color: #1a4a7a; font-size: 30px; font-weight: 700; text-align: center; margin-bottom: 0px; }
    .cpf-cliente { color: #6c757d; font-size: 15px; text-align: center; margin-top: 0px; margin-bottom: 30px; }

    /* Estilo dos Botões Grandes */
    .stButton > button {
        width: 100%;
        height: 100px;
        background-color: #ffffff;
        color: #1a4a7a;
        border: 2px solid #1a4a7a;
        border-radius: 15px;
        font-size: 18px;
        font-weight: 600;
        transition: 0.3s;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 2px 4px 8px rgba(0,0,0,0.05);
    }
    .stButton > button:hover {
        background-color: #1a4a7a;
        color: white;
        transform: translateY(-3px);
    }

    /* Alerta Amarelo Coeso */
    .status-badge {
        background-color: #fff3cd;
        color: #856404;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #ffeeba;
        float: right;
    }

    .card-processo {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #e1e8ed;
        box-shadow: 1px 2px 5px rgba(0,0,0,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS SIMULADA ---
# Somente aceita este CPF/CNH específico para o teste
DB_CLIENTES = {
    "79897789120": {
        "nome": "Edimar",
        "processos": [
            "0737767-85.2025.8.07.0001",
            "0757632-94.2025.8.07.0001",
            "0722313-65.2025.8.07.0001",
            "0768584-35.2025.8.07.0001",
            "0764797-95.2025.8.07.0001"
        ],
        "acordos": []
    }
}

# --- LÓGICA DE SESSÃO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.image("1000423374.jpg", use_container_width=True)

    st.markdown("<h2 style='text-align: center; color: #1a4a7a;'>Acesso Restrito</h2>", unsafe_allow_html=True)
    cpf_input = st.text_input("", placeholder="Insira seu CPF ou CNH", key="login_field")

    if st.button("Entrar no Sistema"):
        if cpf_input in DB_CLIENTES:
            st.session_state.logado = True
            st.session_state.user_cpf = cpf_input
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")

# --- ÁREA DO CLIENTE ---
else:
    cliente = DB_CLIENTES[st.session_state.user_cpf]

    st.markdown(f"<p class='nome-cliente'>Bem-vindo, {cliente['nome']}!</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='cpf-cliente'>ID: {st.session_state.user_cpf}</p>", unsafe_allow_html=True)

    # Botões de Ação
    col_a, col_b = st.columns(2)

    with col_a:
        btn_proc = st.button("⚖️\nProcessos")
    with col_b:
        btn_acor = st.button("🤝\nAcordos")

    # Área de Resultados
    st.markdown("<br>", unsafe_allow_html=True)

    if btn_proc:
        st.subheader("Seus Processos")
        for p in cliente['processos']:
            st.markdown(f"""
                <div class="card-processo">
                    <span class="status-badge">Aguardando Atualização</span>
                    <small style="color: gray;">NÚMERO DO PROCESSO</small><br>
                    <strong>{p}</strong>
                </div>
            """, unsafe_allow_html=True)

    if btn_acor:
        st.subheader("Acordos Judiciais")
        if not cliente['acordos']:
            st.info("Não existem acordos pendentes ou finalizados para este CPF.")

    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()