import streamlit as st
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Amorim & Souza", layout="centered")

# --- FUNÇÃO PARA CARREGAR IMAGEM ---
def get_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

img_b64 = get_base64("1000423374.jpg")

# --- CSS DE ALTA FIDELIDADE (AZUL CLARO / BORDAS AZUIS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* 1. Reset e Fundo Azulado quase branco */
    .stApp {{
        background-color: #F0F7FF !important;
        font-family: 'Inter', sans-serif !important;
    }}

    /* 2. Container Centralizado 420px */
    [data-testid="stMainViewContainer"] > div:first-child {{
        max-width: 420px !important;
        margin: 0 auto !important;
        background-color: #F0F7FF !important;
    }}

    /* 3. Remoção de Lixo Nativo */
    [data-testid="stHeader"], footer, #MainMenu {{
        display: none !important;
    }}

    /* 4. Logo Circular com Borda Azul */
    .logo-container {{
        display: flex;
        justify-content: center;
        padding-top: 50px;
        margin-bottom: 30px;
    }}
    .logo-img {{
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #1A4A7A;
        box-shadow: 0 10px 20px rgba(26, 74, 122, 0.15);
    }}

    /* 5. Inputs Arredondados e Centralizados */
    div[data-testid="stTextInput"] input {{
        border-radius: 12px !important;
        height: 55px !important;
        text-align: center !important;
        border: 2px solid #1A4A7A !important;
        background-color: white !important;
        font-size: 16px !important;
    }}

    /* 6. Botão de Login (Azul Escuro, 60px) */
    div.stButton > button {{
        width: 100% !important;
        background-color: #1A4A7A !important;
        color: white !important;
        border-radius: 12px !important;
        height: 60px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 8px 15px rgba(26, 74, 122, 0.3) !important;
        text-transform: uppercase;
    }}

    /* 7. Botões Dashboard Lado a Lado */
    .stButton > button[kind="secondary"] {{
        background-color: white !important;
        color: #1A4A7A !important;
        border: 2px solid #1A4A7A !important;
        height: 100px !important;
        font-weight: 600 !important;
    }}

    /* 8. Card de Processos com Tag Amarela */
    .p-card {{
        background: white;
        border: 1px solid #1A4A7A;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        position: relative;
    }}
    .status-tag {{
        position: absolute;
        top: 10px;
        right: 10px;
        background: #FFD700;
        color: #000;
        font-size: 9px;
        font-weight: 900;
        padding: 4px 8px;
        border-radius: 4px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGAÇÃO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'tela' not in st.session_state:
    st.session_state.tela = 'login'

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown(f'<div class="logo-container"><img src="data:image/jpeg;base64,{img_b64}" class="logo-img"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; color: #1A4A7A; margin-bottom: 40px;'>Amorim & Souza</h2>", unsafe_allow_html=True)
    
    cpf = st.text_input("CPF", placeholder="Digite seu CPF", label_visibility="collapsed")
    
    if st.button("LOGIN"):
        if cpf == "79897789120":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")

# --- TELA DASHBOARD ---
else:
    st.markdown("<h2 style='color: #1A4A7A;'>Olá, Edimar</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📄\nPROCESSOS", key="p_btn"):
            st.session_state.tela = 'processos'
    with col2:
        if st.button("🤝\nACORDOS", key="a_btn"):
            st.warning("Em atualização")

    if st.session_state.tela == 'processos':
        procs = ["0737767-85.2025.8.07.0001", "0757632-94.2025.8.07.0001", "0722313-65.2025.8.07.0001", "0768584-35.2025.8.07.0001", "0764797-95.2025.8.07.0001"]
        for p in procs:
            st.markdown(f"""
                <div class="p-card">
                    <div class="status-tag">AGUARDANDO ATUALIZAÇÃO</div>
                    <div style="font-size: 10px; color: #1A4A7A;">Número do Processo</div>
                    <div style="font-weight: 700; color: #333;">{p}</div>
                </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("SAIR"):
        st.session_state.logado = False
        st.session_state.tela = 'login'
        st.rerun()
