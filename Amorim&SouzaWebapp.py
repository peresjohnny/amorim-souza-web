import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Amorim & Souza", layout="centered")

# --- CSS PARA INTERFACE PREMIUM MOBILE-FIRST ---
st.markdown("""
    <style>
    /* Importação da fonte Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    /* 1. Reset de Layout e Fundo */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', sans-serif;
    }

    /* 2. Forçar Container 420px Centralizado */
    [data-testid="stMainViewContainer"] > div:first-child {
        max-width: 420px !important;
        margin: 0 auto !important;
        background-color: #F8FAFC !important;
    }

    /* 3. Remoção de Elementos Nativos */
    header, footer, [data-testid="stSidebar"], #MainMenu {
        display: none !important;
        visibility: hidden !important;
    }

    /* 4. Estilização da Logo (Centralizada e Circular) */
    .logo-wrapper {
        display: flex;
        justify-content: center;
        padding: 30px 0 10px 0;
    }
    .logo-img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 2px solid #1A4A7A;
    }

    /* 5. Inputs Arredondados e Centralizados */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important;
        height: 55px !important;
        text-align: center !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 16px !important;
    }

    /* 6. Botão de Login (Azul Escuro, Sombra, 60px) */
    div.stButton > button {
        width: 100% !important;
        background-color: #1A4A7A !important;
        color: white !important;
        border-radius: 12px !important;
        height: 60px !important;
        font-weight: 700 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(26, 74, 122, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* 7. Cards de Processos */
    .card-processo {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #EDF2F7;
        position: relative;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .tag-atualizacao {
        position: absolute;
        top: 12px;
        right: 12px;
        background-color: #FEF08A;
        color: #854D0E;
        font-size: 9px;
        font-weight: 800;
        padding: 4px 8px;
        border-radius: 4px;
    }

    /* 8. Botões Dashboard Lado a Lado */
    .stButton > button[kind="secondary"] {
        background-color: white !important;
        color: #1A4A7A !important;
        border: 1px solid #E2E8F0 !important;
        height: 80px !important;
        box-shadow: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGAÇÃO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'

# --- TELA DE LOGIN ---
if not st.session_state.logado:
    st.markdown('<div class="logo-wrapper"><img src="https://raw.githubusercontent.com/username/repo/main/1000423374.jpg" class="logo-img" onerror="this.src=\'https://via.placeholder.com/150\'"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: #1A4A7A; font-weight: 700;'>Amorim & Souza Advogados</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B; margin-top: -15px;'>Consulta de Andamento Processual</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    cpf_input = st.text_input("CPF", placeholder="Digite seu CPF (apenas números)", label_visibility="collapsed")
    
    if st.button("ACESSAR PROCESSOS"):
        if cpf_input == "79897789120":
            st.session_state.logado = True
            st.rerun()
        else:
            st.error("CPF não cadastrado na base de dados.")
    
    st.markdown("<p style='text-align: center; color: #94A3B8; font-size: 12px; margin-top: 50px;'>Amorim & Souza © 2026 - Sistema exclusivo para clientes.</p>", unsafe_allow_html=True)

# --- ÁREA INTERNA (DASHBOARD) ---
else:
    st.markdown("<h2 style='text-align: center; color: #1A4A7A; padding-top: 20px;'>Olá, Edimar</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📂\nProcessos", key="btn_proc"):
            st.session_state.pagina = 'processos'
    with col2:
        if st.button("🤝\nAcordos", key="btn_acor"):
            st.warning("Em atualização")

    # Exibição de Processos
    if st.session_state.pagina == 'processos':
        st.markdown("<br>", unsafe_allow_html=True)
        lista_processos = [
            "0737767-85.2025.8.07.0001", "0757632-94.2025.8.07.0001",
            "0722313-65.2025.8.07.0001", "0768584-35.2025.8.07.0001",
            "0764797-95.2025.8.07.0001"
        ]
        
        for proc in lista_processos:
            st.markdown(f"""
                <div class="card-processo">
                    <span class="tag-atualizacao">AGUARDANDO ATUALIZAÇÃO</span>
                    <div style="font-size: 11px; color: #94A3B8;">Número do Processo</div>
                    <div style="font-weight: 600; color: #1E293B; margin-top: 4px;">{proc}</div>
                </div>
            """, unsafe_allow_html=True)

    if st.button("SAIR", type="secondary"):
        st.session_state.logado = False
        st.rerun()
