import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Portal Jurídico", layout="centered", initial_sidebar_state="collapsed")

# --- ESTILO CSS PREMIUM MOBILE-FIRST ---
st.markdown("""
    <style>
    /* Importação de Fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* Reset e Esconder Elementos Nativos */
    #MainMenu, footer, header, [data-testid="stSidebarNav"] {vertical-align: hidden; display: none;}
    
    /* Container Principal Mobile-First */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stMainViewContainer"] > div:first-child {
        max-width: 420px !important;
        margin: 0 auto !important;
        background-color: #F8FAFC;
    }

    /* Logo Circular com Sombra */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }
    .logo-img {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }

    /* Inputs Personalizados */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important;
        height: 50px;
        text-align: center;
        border: 1px solid #E2E8F0 !important;
        background-color: white !important;
    }

    /* Botão de Login Estilizado */
    div.stButton > button {
        width: 100% !important;
        background-color: #1A4A7A !important;
        color: white !important;
        border-radius: 12px !important;
        height: 60px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        border: none !important;
        box-shadow: 0 10px 15px -3px rgba(26, 74, 122, 0.3) !important;
        transition: transform 0.2s;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* Botões do Dashboard */
    .dash-btn-container {
        display: flex;
        gap: 10px;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .stButton > button[kind="secondary"] {
        background-color: white !important;
        color: #1A4A7A !important;
        border: 1px solid #E2E8F0 !important;
        height: 100px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* Card de Processos */
    .process-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 12px;
        position: relative;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .status-tag {
        position: absolute;
        top: 10px;
        right: 10px;
        background-color: #FEF08A;
        color: #854D0E;
        font-size: 9px;
        font-weight: 800;
        padding: 4px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    .process-number {
        font-size: 14px;
        font-weight: 600;
        color: #334155;
        margin-top: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE SESSÃO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("1000423374.jpg", width=120)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; color: #1A4A7A;'>Acesso ao Portal</h3>", unsafe_allow_html=True)
    
    cpf_input = st.text_input("CPF", placeholder="000.000.000-00", label_visibility="collapsed")
    
    if st.button("ENTRAR"):
        if cpf_input == "79897789120":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")

# --- DASHBOARD INTERNO ---
else:
    st.markdown("<h2 style='text-align: center; color: #1A4A7A; margin-bottom: 30px;'>Olá, Edimar</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄\n\nProcessos", key="btn_proc", use_container_width=True):
            st.session_state.view = 'processos'
            
    with col2:
        if st.button("🤝\n\nAcordos", key="btn_acod", use_container_width=True):
            st.session_state.view = 'acordos'
            st.warning("Em atualização")

    st.markdown("---")

    # --- LISTAGEM DE PROCESSOS ---
    if st.session_state.view == 'processos':
        processos = [
            "0737767-85.2025.8.07.0001", "0757632-94.2025.8.07.0001",
            "0722313-65.2025.8.07.0001", "0768584-35.2025.8.07.0001",
            "0764797-95.2025.8.07.0001"
        ]
        
        for p in processos:
            st.markdown(f"""
                <div class="process-card">
                    <div class="status-tag">AGUARDANDO ATUALIZAÇÃO</div>
                    <div style="font-size: 10px; color: #64748B;">Número do Processo</div>
                    <div class="process-number">{p}</div>
                </div>
            """, unsafe_allow_html=True)

    if st.button("Sair", type="secondary"):
        st.session_state.logado = False
        st.session_state.view = 'home'
        st.rerun()
