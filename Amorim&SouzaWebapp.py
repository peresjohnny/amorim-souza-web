import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Amorim & Souza", layout="centered")

# --- ESTILO CSS PARA FORMATO DE APP DE CELULAR ---
st.markdown("""
    <style>
    /* Fundo azul muito claro */
    .stApp {
        background-color: #f1f6fa;
    }
    
    /* Forçar largura de celular no Desktop e centralizar */
    [data-testid="stMainViewContainer"] > div:first-child {
        max-width: 420px;
        margin: 0 auto;
        background-color: #f1f6fa;
        padding-top: 20px;
    }

    /* Títulos */
    .titulo-app {
        color: #1a4a7a;
        font-family: 'Source Sans Pro', sans-serif;
        font-weight: 700;
        text-align: center;
        font-size: 22px;
        margin-top: 10px;
    }

    /* Botão de Login Estilo Mobile */
    .stButton > button {
        width: 100%;
        background-color: #1a4a7a;
        color: white !important;
        border-radius: 10px;
        height: 55px;
        font-size: 18px;
        font-weight: 600;
        border: none;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background-color: #143a5f;
        border: none;
    }

    /* Inputs arredondados */
    .stTextInput > div > div > input {
        border-radius: 10px;
        height: 50px;
        border: 1px solid #dce4ec;
        text-align: center;
    }

    /* Ajuste da Logo */
    .stImage > img {
        border-radius: 50%;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }

    /* Esconder elementos nativos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DADOS SIMULADA ---
DB_CLIENTES = {
    "79897789120": {
        "nome": "Edimar",
        "processos": [
            "0737767-85.2025.8.07.0001",
            "0757632-94.2025.8.07.0001",
            "0722313-65.2025.8.07.0001",
            "0768584-35.2025.8.07.0001",
            "0764797-95.2025.8.07.0001"
        ]
    }
}

if 'logado' not in st.session_state:
    st.session_state.logado = False

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Logo Centralizada
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("1000423374.jpg", use_container_width=True)
    
    st.markdown("<p class='titulo-app'>Amorim & Souza Advogados</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #1a4a7a; font-size: 14px;'>Portal de Consulta Processual</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Input de CPF
    cpf_input = st.text_input("CPF ou CNH", placeholder="Digite apenas números")
    
    if st.button("Login"):
        if cpf_input in DB_CLIENTES:
            st.session_state.logado = True
            st.session_state.user_cpf = cpf_input
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")
    
    st.markdown("<br><br><p style='text-align: center; color: #bdc3c7; font-size: 11px;'>© 2026 Amorim & Souza - Todos os direitos reservados.</p>", unsafe_allow_html=True)

# --- ÁREA LOGADA ---
else:
    cliente = DB_CLIENTES[st.session_state.user_cpf]
    st.markdown(f"<h2 style='text-align: center; color: #1a4a7a;'>Olá, {cliente['nome']}!</h2>", unsafe_allow_html=True)
    
    # Adicione aqui o restante da lógica de botões que definimos antes
    if st.button("Sair"):
        st.session_state.logado = False
        st.rerun()
